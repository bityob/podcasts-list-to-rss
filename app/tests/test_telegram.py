import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from app.telegram import TelegramReader


@pytest.mark.asyncio
async def test_gen_messages():
    r = TelegramReader()
    
    messages = [m async for m in r.gen_messages()]
    
    assert messages