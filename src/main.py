import urllib3
from loguru import logger

from src.rss import RssGenerator
from src.settings import RSS_FILE_PATH
from telegram import TelegramReader

urllib3.disable_warnings()


def main():
    logger.info("Starting...")

    reader = TelegramReader()

    messages = [m for m in reader.gen_messages()]

    rss = RssGenerator(messages)

    rss_text = rss.create_rss()

    with open(RSS_FILE_PATH, "w", encoding="utf-8") as writer:
        writer.write(rss_text)

    logger.info("Done.")


if __name__ == "__main__":
    main()
