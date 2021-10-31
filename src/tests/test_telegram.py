from unittest import IsolatedAsyncioTestCase, mock

import pytest

from .telegram import TelegramReader


@pytest.mark.asyncio
@mock.patch('src.telegram.TelegramClient')
async def test_gen_messages(self, client):
    reader = TelegramReader()

    messages = [m async for m in reader.gen_messages()]