import os
from typing import Iterable, Optional

from telethon import TelegramClient

from base import Message


api_id = os.environ["TELEGRAM_APP_ID"]
api_hash = os.environ["TELEGRAM_APP_HASH"]
channel_name = os.environ["TELEGRAM_PUBLIC_CHANNEL_NAME"]
phone = os.environ["TELEGRAM_PHONE"]
password = os.environ["TELEGRAM_PASSWORD"]


class TelegramReader:
    @staticmethod
    async def get_url_from_message(message) -> Optional[str]:
        if message.web_preview:
            return message.web_preview.url
        return None

    async def gen_messages(self) -> Iterable[Message]:
        async with TelegramClient('user', api_id, api_hash) as client:
            await client.start(
                phone=phone,
                password=password,
            )

            async for message in client.iter_messages(channel_name, limit=100):
                print(f"id={message.id}, date={message.date}")
                if message.text:
                    yield Message(
                        id=message.id,
                        url=await self.get_url_from_message(message), 
                        text=message.text,
                        date=message.date,
                    )


