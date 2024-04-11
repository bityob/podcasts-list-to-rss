from dataclasses import dataclass
from datetime import datetime
from functools import cached_property

from requests_html import Element, HTMLSession
from telethon.tl.types import Document

session = HTMLSession()


class RssConnector:
    def __init__(self, url: str):
        self.url = url
        self.session = session
        self.request = self.session.get(self.url, verify=False)
        self.request.raise_for_status()
        self.html = self.request.html

    def _get_rss_feed(self) -> str:
        """
        Returns the RSS feed for this url
        """
        raise NotImplementedError()

    def _get_rss_item(self) -> Element:
        """
        Returns an xml extracted from the RSS feed
        """
        raise NotImplementedError()

    def _get_item_title(self) -> str:
        raise NotImplementedError()

    @cached_property
    def rss_feed(self) -> str:
        return self._get_rss_feed()

    @cached_property
    def item_title(self) -> str:
        return self._get_item_title()

    @cached_property
    def item(self) -> str:
        return self._get_rss_item()


@dataclass
class Message:
    id: int
    text: str
    url: str | None
    date: datetime
    urls: list[str]
    audio: Document
