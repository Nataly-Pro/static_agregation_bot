from unittest.mock import AsyncMock

import pytest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram3_calendar import DialogCalendar

from bot.handlers.command_handlers import process_dialog_calendar, command_type, command_start
from bot.keyboards import inline_keyboard
from bot.lexicon import LEXICON
from tests.test_handlers.utils import TEST_USER, TEST_USER_CHAT, get_update


@pytest.mark.asyncio
async def test_command_start():
    message = AsyncMock()
    await command_start(message)
    message.answer.assert_called_with(text=LEXICON['/start'])


@pytest.mark.asyncio
async def test_process_dialog_calendar(storage, bot):
    callback_query = AsyncMock()
    callback_data = AsyncMock()
    state = FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id,
                       user_id=TEST_USER.id,
                       chat_id=TEST_USER_CHAT.id)
    )
    await process_dialog_calendar(callback_query=callback_query,
                                  callback_data=callback_data,
                                  state=state)
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    assert await state.get_state() == date


@pytest.mark.asyncio
async def test_command_type(storage, bot):
    message = AsyncMock()
    state = FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id,
                       user_id=TEST_USER.id,
                       chat_id=TEST_USER_CHAT.id)
    )
    await command_type(message=message, state=state)
    message.answer.assert_called_with(text='Выберите тип группировки данных: ',
                                      reply_markup=inline_keyboard)


