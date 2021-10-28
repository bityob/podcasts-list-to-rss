from typing import List

from lxml import etree
from podgen import Podcast, Episode
from podgen.util import formatRFC2822

from base import Message
from pocket_casts import PocketCasts
from requests_xml import XML

CLOSING_CHANNEL_TAG = "</channel>"

name = "פודקאסט פלייליסט"
description = """ערוץ עידכוני הפרקים של יוליה שנרר. כאן תמצאו המלצות על פרקים מפודקאסטים שונים. אין סדר או העדפה מסוימים, מה שנשמע מעניין באותו שבוע.

ניתן לחפש בערוץ בעזרת האשתגים: #שיווק #כלכלה ועוד... 

דברו איתי כאן:
https://www.linkedin.com/in/yuliashnerer"""
website = "https://t.me/podcastsrec"


class RssGenerator:
    def __init__(self, messages: List[Message]):
        self.p = Podcast(
            name=name,
            description=description,
            website=website,
            explicit=False,
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

        for message in reversed(self.messages):
            try:
                print(f"Message id={message.id}...")
                connector = PocketCasts(message.url)
                print(f"title={connector.item_title}")

                item = str(connector.item)
                        
                # Replace item fields
                xml_item = XML(xml=item)

                xml_item.lxml.find("pubDate").text = formatRFC2822(message.date)
                
                print(f"after={xml_item.lxml.find('pubDate').text}")

                # Must use the `lxml` and not the `xml`, because we change it 
                xml_string = etree.tostring(xml_item.lxml, encoding='utf8').decode('utf8')

                rss_string = rss_string.replace(CLOSING_CHANNEL_TAG, f"{xml_string}{CLOSING_CHANNEL_TAG}")
            except Exception as ex:
                # raise
                print(f"Failed with message id={message.id}, error={ex}")


        return rss_string
