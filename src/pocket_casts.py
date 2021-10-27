from typing import Optional

from requests_html import HTML, Element

from base import RssConnector 


class PocketCasts(RssConnector):
    """
    Link example: https://pca.st/29rqw2h4
    """
    def _get_rss_feed(self) -> str:
        return self.html.find('.rss_button', first=True).links.pop()

    def _get_rss_item(self) -> Element:
        r = self.session.get(self.rss_feed, verify=False)
        item = self._get_item_from_html(html=r.html, title_text=self.item_title)
        
        if not item:
            raise RuntimeError(f"Failed to get the item for title \
                                '{self.item_title}' from RSS feed '{self.rss_feed}'")

        return item

    def _get_item_from_html(self, html: HTML, title_text: str) -> Optional[Element]:
        for item in html.find('item'):
            curr_title = item.find('title', first=True).text
            if curr_title == title_text:
                return item.html
        return None

    def _get_item_title(self):
        return self.html.find('.section > h1', first=True).text

        

