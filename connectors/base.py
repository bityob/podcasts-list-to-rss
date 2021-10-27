from functools import cached_property

from requests_html import HTMLSession, Element

session = HTMLSession()


class RssConnector:
    def __init__(self, url: str):
        self.url = url
        self.request = session.get(self.url)
        self.request.raise_for_status()
        self.html = self.request.html

    def _get_rss_feed(self) -> str:
        """
        Returns the RSS feed for this url
        """
        raise NotImplemented()

    def _get_rss_item(self) -> Element:
        """
        Returns an xml extracted from the RSS feed
        """
        raise NotImplemented()

    def _get_item_title() -> str:
        raise NotImplemented()

    @cached_property
    def rss_feed(self) -> str:
        return self._get_rss_feed()

    @cached_property
    def item_title(self) -> str:
        return self._get_item_title()