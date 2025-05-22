import re
from functools import cached_property

from requests_html import HTMLSession
from requests_xml import XML, Element, XMLSession

from base import RssConnector
from src.db import Episode, MessageLink, RssFeed


class PocketCasts(RssConnector):
    url_host = "pca.st"
    response_url_pattern = re.compile(r"https://play.pocketcasts.com/podcasts/([a-z0-9\-]+)/([a-z0-9\-]+)")
    podcasts_data_url = "https://podcast-api.pocketcasts.com/podcast/full/{podcast_id}"
    """
    Link example:
        https://pca.st/29rqw2h4
        https://pca.st/episode/a2b71564-2b70-4f1f-b487-c61ffd2702a8
    """
    session = HTMLSession()
    xml_session = XMLSession()

    def __init__(self, url, message_id):
        self.url = url
        self.message_id = message_id

        self.podcast_id = None
        self.episode_id = None
        self.podcast_name = None
        self._item_title = None
        self._rss_feed = None
        self._rss_item = None

        self.message_in_db = (
            MessageLink.select(MessageLink, Episode, RssFeed)
            .join(Episode)
            .join(RssFeed)
            .where(
                (MessageLink.message_id == self.message_id)
                & (MessageLink.link == self.url)
                & (Episode.podcast_id == RssFeed.podcast_id)
            )
        ).get_or_none()

        if self.message_in_db:
            self.podcast_id = self.message_in_db.episode.podcast_id
            self.episode_id = self.message_in_db.episode.episode_id
            self.podcast_name = self.message_in_db.episode.podcast.podcast_name
            self._item_title = self.message_in_db.episode.episode_name
            self._rss_feed = self.message_in_db.episode.podcast.rss_feed
            self._rss_item = self.message_in_db.rss_item

        self.get_missing_episode_data_and_store_in_db()

    @classmethod
    def get_podcast_id_from_response_url(cls, url: str) -> tuple[str, str]:
        if m := cls.response_url_pattern.match(url):
            return m.groups()  # type: ignore
        raise ValueError(f"Url response is not valid: {url}")

    def get_episode_and_podcast_ids(self):
        # Get podcast id and episode id
        if not self.podcast_id or not self.episode_id:
            self.response = self.session.get(self.url)
            self.response.raise_for_status()
            self.podcast_id, self.episode_id = self.get_podcast_id_from_response_url(self.response.url)

    def _get_rss_feed(self) -> str:
        if self._rss_feed and self.podcast_name:
            return self._rss_feed

        if not self._rss_feed:
            json_data = {
                "uuids": self.podcast_id,
            }
            response = self.session.post("https://refresh.pocketcasts.com/import/export_feed_urls", json=json_data)
            response.raise_for_status()

        RssFeed.insert(
            podcast_id=self.podcast_id,
            rss_feed=self._rss_feed or response.json()["result"][self.podcast_id],
            podcast_name=self.podcast_name or self.podcast_data["title"],
        ).on_conflict("ignore").execute()

        rss_feed_obj = RssFeed.get_or_none(RssFeed.podcast_id == self.podcast_id)
        self._rss_feed = rss_feed_obj.rss_feed
        self.podcast_name = rss_feed_obj.podcast_name

        return self._rss_feed

    def _get_rss_item(self) -> Element:
        if not self._rss_item:
            r = self.xml_session.get(self.rss_feed)
            item = self._get_item_from_xml(xml=r.xml, title_text=self.item_title)

            if not item:
                raise RuntimeError(
                    f"Failed to get the item for title '{self.item_title}' from RSS feed '{self.rss_feed}'"
                )

            MessageLink.insert(
                message_id=self.message_id,
                link=self.url,
                episode_id=self.episode_id,
                rss_item=item,
            ).on_conflict(
                conflict_target=[MessageLink.message_id, MessageLink.link],
                preserve=[MessageLink.episode_id, MessageLink.rss_item],
            ).execute()
            self._rss_item = item

        return self._rss_item

    def _get_item_title(self):
        if not self._item_title:

            # Get all episodes and save to db
            episodes = self.podcast_data["episodes"]
            Episode.insert_many(
                [
                    {
                        "podcast_id": self.podcast_id,
                        "episode_id": x["uuid"],
                        "episode_name": x["title"],
                    }
                    for x in episodes
                ]
            ).on_conflict("ignore").execute()
            self._item_title = Episode.get_or_none(Episode.episode_id == self.episode_id).episode_name
        return self._item_title

    @cached_property
    def podcast_data(self):
        response = self.session.get(self.podcasts_data_url.format(podcast_id=self.podcast_id))
        response.raise_for_status()
        podcast_data = response.json()["podcast"]
        return podcast_data

    def _get_item_from_xml(self, xml: XML, title_text: str) -> Element | None:
        for item in xml.find("item"):
            curr_title = item.find("title", first=True).text
            if curr_title == title_text:
                return item.xml

        # Sometimes the title match the itunes title only, check from there if not found
        for item in xml.find("item"):
            curr_title = item.lxml.find("itunes:title", namespaces=item.lxml.nsmap).text
            if curr_title == title_text:
                return item.xml
            if curr_title.strip() == title_text:
                return item.xml

        return None

    @classmethod
    def is_valid_url(cls, url):
        if url is not None:
            return cls.url_host in url
        return False

    def get_missing_episode_data_and_store_in_db(self):
        self.get_episode_and_podcast_ids()
        self._get_rss_feed()
        self._get_item_title()
        self._get_rss_item()
