import asyncio

from telegram import TelegramReader

async def main():
    reader = TelegramReader()

    async for message in reader.gen_messages():
        print(message)    


if __name__ == '__main__':
    asyncio.run(main())