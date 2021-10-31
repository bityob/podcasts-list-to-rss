import asyncio
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock, patch

import pytest

from app.telegram import TelegramReader


@pytest.fixture(scope="class")
def event_loop_instance(request):
    """ Add the event_loop as an attribute to the unittest style test class. """
    request.cls.event_loop = asyncio.get_event_loop_policy().new_event_loop()
    yield
    request.cls.event_loop.close()


@pytest.mark.usefixtures("event_loop_instance")
class TestTheThings(TestCase):

    def get_async_result(self, coro):
        """ Run a coroutine synchronously. """
        return self.event_loop.run_until_complete(coro)

    def test_an_async_method(self):
        reader = TelegramReader()

        result = self.get_async_result(list(reader.gen_messages()))
        # result is the actual result, so whatever assertions..
        # self.assertEqual(result,  "banana")


# @pytest.mark.usefixtures("event_loop_instance")
# @patch('app.telegram.TelegramClient', new_callable=AsyncMock)
# def test_gen_messages(self):
#     reader = TelegramReader()
    
#     asyncio.event_loop.run_until_complete(reader.gen_messages())

