import os
from typing import Iterable, Optional
import re

from telethon import TelegramClient

from src.base import Message
from src.settings import RSS_MAX_MESSAGES, TELEGRAM_APP_ID, TELEGRAM_APP_HASH, CHANNEL_NAME, PUBLIC_DOWNLOAD_URL_BOT

URL_PATTERN = r"(https?://[^\s]+)"

url_regex = re.compile(URL_PATTERN)


class TelegramReader:
    @staticmethod
    async def get_urls_from_text_message(message) -> Optional[str]:
        return url_regex.findall(message.text)
    
    @staticmethod
    async def get_url_from_message(message) -> Optional[str]:
        if message.web_preview:
            return message.web_preview.url
        return None

    async def gen_messages(self) -> Iterable[Message]:
        async with TelegramClient('user', TELEGRAM_APP_ID, TELEGRAM_APP_HASH, timeout=5) as client:
            await client.start()

            async for message in client.iter_messages(CHANNEL_NAME, limit=RSS_MAX_MESSAGES, wait_time=5):
                print(f"id={message.id}, date={message.date}")
                if message.text:
                    yield Message(
                        id=message.id,
                        url=await self.get_url_from_message(message), 
                        urls=await self.get_urls_from_text_message(message),
                        text=message.text,
                        audio=message.audio,
                        date=message.date,
                    )

    @staticmethod
    async def get_download_url(message):
        async with TelegramClient('user', TELEGRAM_APP_ID, TELEGRAM_APP_HASH) as client:
            await client.start()

            await client.forward_messages(PUBLIC_DOWNLOAD_URL_BOT, message)
