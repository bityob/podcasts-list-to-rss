import re
from collections.abc import Generator

from loguru import logger
from telethon import TelegramClient

from src.base import Message
from src.db import MessageLink
from src.settings import (
    CHANNEL_NAME,
    CHECK_FOR_NEW_MESSAGES_ONLY,
    PUBLIC_DOWNLOAD_URL_BOT,
    RSS_MAX_MESSAGES,
    TELEGRAM_APP_HASH,
    TELEGRAM_APP_ID,
)

URL_PATTERN = r"(https?://[^\s\])]+)"

url_regex = re.compile(URL_PATTERN)


class TelegramReader:
    @staticmethod
    def get_urls_from_text_message(message) -> list[str]:
        return url_regex.findall(message.text.replace("*", ""))

    @staticmethod
    def get_url_from_message(message) -> str | None:
        if message.web_preview:
            return message.web_preview.url
        return None

    def gen_messages(self) -> Generator[Message, None, None]:
        min_message_id = 0

        if CHECK_FOR_NEW_MESSAGES_ONLY:
            min_message_id = MessageLink.select().order_by(MessageLink.message_id.desc()).get().message_id

        with TelegramClient("user", TELEGRAM_APP_ID, TELEGRAM_APP_HASH, timeout=5) as client:
            client.start()

            for message in client.iter_messages(
                CHANNEL_NAME, limit=RSS_MAX_MESSAGES, wait_time=5, min_id=min_message_id + 1
            ):
                logger.info(f"id={message.id}, date={message.date}")
                if message.text:
                    yield Message(
                        id=message.id,
                        url=self.get_url_from_message(message),
                        urls=self.get_urls_from_text_message(message),
                        text=message.text,
                        audio=message.audio,
                        date=message.date,
                        message_url=f"https://t.me/{CHANNEL_NAME}/{message.id}",
                    )

    @staticmethod
    async def get_download_url(message):
        async with TelegramClient("user", TELEGRAM_APP_ID, TELEGRAM_APP_HASH) as client:
            await client.start()

            await client.forward_messages(PUBLIC_DOWNLOAD_URL_BOT, message)
