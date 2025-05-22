import traceback
from pathlib import Path

from loguru import logger
from lxml import etree
from podgen import Podcast
from podgen.util import formatRFC2822
from requests_xml import XML

from base import Message
from pocket_casts import AlreadyFailedMessage, PocketCasts
from src.db import Error
from src.settings import (
    CHECK_FOR_NEW_MESSAGES_ONLY,
    RSS_DESCRIPTION,
    RSS_FILE_PATH,
    RSS_IMAGE_URL,
    RSS_NAME,
    RSS_WEBSITE,
)
from src.utils import timer

CLOSING_CHANNEL_TAG = "</channel>"
ITEM_TAG = "<item"


class RssGenerator:
    def __init__(self, messages: list[Message]):
        self.p = Podcast(
            name=RSS_NAME,
            description=RSS_DESCRIPTION,
            website=RSS_WEBSITE,
            explicit=False,
            image=RSS_IMAGE_URL,
        )
        self.messages = messages
        if CHECK_FOR_NEW_MESSAGES_ONLY:
            self.messages = reversed(self.messages)

    def create_rss(self):
        """
        Need to take the original xml item string and change only those fields:
        * pubDate - use telegram Message date
        * description - prepand the orignal text with the Message text
        """
        # Rss with only basic fields
        rss_string = str(self.p)

        if CHECK_FOR_NEW_MESSAGES_ONLY:
            rss_string = Path(RSS_FILE_PATH).read_text()

        for message in self.messages:
            logger.info(f"Message id={message.id}...")

            all_urls = message.urls

            valid_urls = [url for url in all_urls if PocketCasts.is_valid_url(url)]

            found_url = valid_urls[0] if valid_urls else None

            logger.info(f"Found url={found_url}")

            # TODO: Add support for messages with audio in Telegram as source for podcasts
            # if message.audio:
            #     logger.info(f"Found audio attached to message: {message.audio}")
            #     TelegramReader.get_download_url(message)
            #     continue

            if found_url is None:
                logger.info(f"Ignoring message {message.id}, text: {message.text} no url found")
                continue

            logger.info(f"Valid urls: {valid_urls}")

            # We iterate over the urls in reversed mode, since usually the urls are in ASC order,
            # and we add the episodes on DESC order here (from the newest to the oldest)
            # Update (22-05-25):
            #   We reverse only when we iterate over all messages, so we are going from END to START,
            #   but when we add only the new messages, we add them from END to START, so we don't reverse the urls,
            #   but reverse the messages
            if not CHECK_FOR_NEW_MESSAGES_ONLY:
                valid_urls = reversed(valid_urls)

            for curr_url in valid_urls:
                try:
                    logger.info(f"Converting url={curr_url} to rss item")
                    rss_string = self.convert_found_url_to_rss_item(curr_url, message, rss_string)
                except AlreadyFailedMessage:
                    logger.info(f"Skipping already failed message; id={message.id}, url={curr_url}")
                    continue
                except Exception as ex:
                    logger.info(f"Failed with message id={message.id}, url={curr_url}, error={ex}")
                    traceback.print_exc()

                    Error.insert(
                        message_id=message.id,
                        link=curr_url,
                        exception_type=ex.__class__.__name__,
                        exception_message=str(ex),
                        exception_traceback=traceback.format_exc(),
                    ).on_conflict("ignore").execute()

                # Enable for debugging
                # raise

            # break

        # Beautify XML
        from lxml import etree

        def beautify_xml(xml_string):
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.fromstring(xml_string, parser)
            return etree.tostring(tree, pretty_print=True, encoding="unicode")

        return beautify_xml(rss_string)

    def convert_found_url_to_rss_item(self, found_url, message, rss_string):
        # TODO: Add logic to use RssConnector based on the message
        #   If link from "pca.st" use PocketsCasts
        #   If audio file attached, take it from there,
        #   and add the description and episode details from the message itself

        with timer("pocket_init"):
            connector = PocketCasts(found_url, message=message)

        logger.info(f"title={connector.item_title}")

        item = str(connector.item)

        # Replace item fields
        # Replace publish date
        xml_item = XML(xml=item)

        try:
            self.update_publish_date(message, xml_item)
        except AttributeError:
            # Sometimes pubDate is in lower
            self.update_publish_date(message, xml_item, "pubdate")

        # Prepand text to description
        original_text = xml_item.lxml.find("description").text

        message_text = message.text.replace("\n", "<br>")

        new_text = f"{message_text}<br><br><br>#######<br><br><br>{original_text}"

        xml_item.lxml.find("description").text = new_text

        try:
            itunes_summary = xml_item.lxml.find("itunes:summary", namespaces=xml_item.lxml.nsmap)
            if itunes_summary is not None:
                itunes_summary.text = new_text
        except Exception:
            pass

        try:
            content_encoded = xml_item.lxml.find("content:encoded", namespaces=xml_item.lxml.nsmap)
            if content_encoded is not None:
                content_encoded.text = new_text
        except Exception:
            pass

        # Must use the `lxml` and not the `xml`, because we change it
        xml_string = etree.tostring(xml_item.lxml, encoding="utf8").decode("utf8")

        if not CHECK_FOR_NEW_MESSAGES_ONLY:
            # We apply all messages from new to old, so we put current one at the end
            rss_string = rss_string.replace(CLOSING_CHANNEL_TAG, f"{xml_string}{CLOSING_CHANNEL_TAG}")
        else:
            # We apply only NEW messages so we put the current one at the beginning, and running on messages reversed
            rss_string = rss_string.replace(ITEM_TAG, f"{xml_string}{ITEM_TAG}")

        return rss_string

    def update_publish_date(self, message, xml_item, tag="pubDate"):
        xml_item.lxml.find(tag).text = formatRFC2822(message.date)
        logger.info(f"after={xml_item.lxml.find(tag).text}")
