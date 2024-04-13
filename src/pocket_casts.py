from requests_xml import XML, Element, XMLSession

from base import RssConnector

xml_session = XMLSession()


class PocketCasts(RssConnector):
    url_host = "pca.st"

    """
    Link example: https://pca.st/29rqw2h4
    """

    def _get_rss_feed(self) -> str:
        return self.html.find(".rss_button", first=True).links.pop()

    def _get_rss_item(self) -> Element:
        r = xml_session.get(self.rss_feed, verify=False)
        item = self._get_item_from_xml(xml=r.xml, title_text=self.item_title)

        if not item:
            raise RuntimeError(f"Failed to get the item for title '{self.item_title}' from RSS feed '{self.rss_feed}'")

        return item

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

        return None

    def _get_item_title(self):
        return self.html.find(".section > h1", first=True).text

    @classmethod
    def is_valid_url(cls, url):
        if url is not None:
            return cls.url_host in url
        return False
