import traceback

from lxml import etree
from podgen import Podcast
from podgen.util import formatRFC2822
from requests_xml import XML

from base import Message
from pocket_casts import PocketCasts
from src.settings import RSS_DESCRIPTION, RSS_IMAGE_URL, RSS_NAME, RSS_WEBSITE

CLOSING_CHANNEL_TAG = "</channel>"


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

    def create_rss(self):
        """
        Need to take the original xml item string and change only those fields:
        * pubDate - use telegram Message date
        * description - prepand the orignal text with the Message text
        """

        # Rss with only basic fields
        rss_string = str(self.p)

        for message in self.messages:
            try:
                print(f"Message id={message.id}...")

                all_urls = message.urls

                valid_urls = [url for url in all_urls if PocketCasts.is_valid_url(url)]

                found_url = valid_urls[0] if valid_urls else None

                print(f"Found url={found_url}")

                # TODO: Add support for messages with audio in Telegram as source for podcasts
                # if message.audio:
                #     print(f"Found audio attached to message: {message.audio}")
                #     TelegramReader.get_download_url(message)
                #     continue

                if found_url is None:
                    print(f"Ignoring message {message.id}, text: {message.text} no url found")
                    continue

                print(f"Valid urls: {valid_urls}")

                # We iterate over the urls in reversed mode, since usually the urls are in ASC order,
                # and we add the episodes on DESC order here (from the newest to the oldest)
                for curr_url in reversed(valid_urls):
                    print(f"Converting url={curr_url} to rss item")
                    rss_string = self.convert_found_url_to_rss_item(curr_url, message, rss_string)

            except Exception as ex:
                print(f"Failed with message id={message.id}, error={ex}, text={message.text}")
                traceback.print_exc()

        return rss_string

    def convert_found_url_to_rss_item(self, found_url, message, rss_string):
        # TODO: Add logic to use RssConnector based on the message
        #   If link from "pca.st" use PocketsCasts
        #   If audio file attached, take it from there,
        #   and add the description and episode details from the message itself
        connector = PocketCasts(found_url)

        print(f"title={connector.item_title}")

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

        rss_string = rss_string.replace(CLOSING_CHANNEL_TAG, f"{xml_string}{CLOSING_CHANNEL_TAG}")

        return rss_string

    def update_publish_date(self, message, xml_item, tag="pubDate"):
        xml_item.lxml.find(tag).text = formatRFC2822(message.date)
        print(f"after={xml_item.lxml.find(tag).text}")
