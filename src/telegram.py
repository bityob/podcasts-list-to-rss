import os

from telethon import TelegramClient

from base import Message


api_id = os.environ["TELEGRAM_APP_ID"]
api_hash = os.environ["TELEGRAM_APP_HASH"]
channel_name = os.environ["TELEGRAM_PUBLIC_CHANNEL_NAME"]


class TelegramReader:
    @staticmethod
    async def get_url_from_message(message) -> str:
        return message.web_preview.url

    async def gen_messages(self):
        async with TelegramClient('user', api_id, api_hash) as client:
            await client.start()

            async for message in client.iter_messages(channel_name):
                yield Message(url=await self.get_url_from_message(message), text=message.text)
                break
                


