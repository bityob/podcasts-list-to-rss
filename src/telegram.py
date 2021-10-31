import os
from typing import Iterable, Optional
import re

from telethon import TelegramClient

from base import Message

URL_PATTERN = r"(https?://[^\s]+)"

api_id = os.environ["TELEGRAM_APP_ID"]
api_hash = os.environ["TELEGRAM_APP_HASH"]
channel_name = os.environ["TELEGRAM_PUBLIC_CHANNEL_NAME"]
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
        async with TelegramClient('user', api_id, api_hash) as client:
            await client.start()

            async for message in client.iter_messages(channel_name, limit=200):
                print(f"id={message.id}, date={message.date}")
                if message.text:
                    yield Message(
                        id=message.id,
                        url=await self.get_url_from_message(message), 
                        urls=await self.get_urls_from_text_message(message),
                        text=message.text,
                        date=message.date,
                    )


