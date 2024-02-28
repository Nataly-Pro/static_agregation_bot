import asyncio

import pytest
import pytest_asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers.command_handlers import command_router
from tests.test_handlers.mocked_bot import MockedBot


@pytest_asyncio.fixture(scope="session")
async def storage():
    tmp_storage = MemoryStorage()
    try:
        yield tmp_storage
    finally:
        await tmp_storage.close()


@pytest.fixture()
def bot():
    return MockedBot()


@pytest_asyncio.fixture()
async def dispatcher():
    dp = Dispatcher()
    dp.include_router(command_router)
    #dp.include_router(formatted_router)
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()


# @pytest.fixture(scope="session")
# def event_loop():
    # asyncio.set_event_loop(asyncio.new_event_loop())
    #return asyncio.get_event_loop()


