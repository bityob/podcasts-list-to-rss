import asyncio
import urllib3
urllib3.disable_warnings()

from lxml import etree
from telegram import TelegramReader
from rss import RssGenerator, LAST_TELEGRAM_MESSAGE_ID_TAG

RSS_FILE_PATH = "assets/rss.xml"


def get_last_fetched_message_id():
    try:
        tree = etree.parse(RSS_FILE_PATH)
        last_message_id = tree.find(f"channel/{LAST_TELEGRAM_MESSAGE_ID_TAG}").text
        return int(last_message_id)
    except Exception as ex:
        print(f"Failed to get message id from RSS, error: {str(ex)}")
        return 0



async def main():    
    reader = TelegramReader()

    messages = [m async for m in reader.gen_messages(first_message=get_last_fetched_message_id())]
    
    if messages:
        rss = RssGenerator(messages)

        rss_text = rss.create_rss()

        with open(RSS_FILE_PATH, 'wt', encoding='utf-8') as writer:
            writer.write(rss_text)
    else:
        print("No new messages...")


if __name__ == '__main__':
    asyncio.run(main())