import asyncio

import urllib3

from src.rss import RssGenerator
from src.settings import RSS_FILE_NAME
from telegram import TelegramReader

urllib3.disable_warnings()


async def main():
    print("Starting...")

    reader = TelegramReader()

    messages = [m async for m in reader.gen_messages()]

    rss = RssGenerator(messages)

    rss_text = rss.create_rss()

    with open(f"/opt/assets/{RSS_FILE_NAME}", "w", encoding="utf-8") as writer:
        writer.write(rss_text)


if __name__ == "__main__":
    asyncio.run(main())
