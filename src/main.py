import asyncio
import urllib3
urllib3.disable_warnings()

from podgen import Podcast, Episode

from telegram import TelegramReader
from rss import RssGenerator



async def main():
    reader = TelegramReader()

    messages = [m async for m in reader.gen_messages()]

    rss = RssGenerator(messages)

    rss_text = rss.create_rss()

    with open('assets/rss.xml', 'wt', encoding='utf-8') as writer:
        writer.write(rss_text)


if __name__ == '__main__':
    asyncio.run(main())