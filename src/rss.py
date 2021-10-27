from typing import List

from lxml import etree
from podgen import Podcast, Episode

from base import Message
from pocket_casts import PocketCasts

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
        # for message in self.messages:
        #     connector = PocketCasts(message.url)
        #     curr_episode = Episode(
        #         title=connector.item_title,
        #         long_summary=message.text,
        #         publication_date=message.date,
        #     )
        #     self.p.episodes.append(curr_episode)

        # Rss with only basic fields
        rss_string = str(self.p)

        for message in reversed(self.messages):
            try:
                print(f"Message id={message.id}...")
                connector = PocketCasts(message.url)
                rss_string = rss_string.replace(CLOSING_CHANNEL_TAG, f"{connector.item}{CLOSING_CHANNEL_TAG}")
            except:
                print(f"Failed with message id={message.id}")

        return rss_string
