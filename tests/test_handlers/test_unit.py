from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from bot.handlers.command_handlers import command_start, command_type, process_group_type, \
    command_report
from bot.keyboards import inline_keyboard
from bot.lexicon import LEXICON
from bot.services import get_report
from tests.test_handlers.utils import TEST_USER_CHAT, TEST_USER


@pytest.mark.asyncio
async def test_command_start(storage, bot):
    """Юнит-тест на то, что функция возвращает корректное сообщение.
    """
    message = AsyncMock()
    state = FSMContext(storage=storage,
                       key=StorageKey(
                           bot_id=bot.id,
                           user_id=TEST_USER.id,
                           chat_id=TEST_USER_CHAT.id))
    await command_start(message=message, state=state)
    assert await state.get_state() is None
    message.answer.assert_called_with(text=LEXICON['/start'])


@pytest.mark.asyncio
async def test_process_group_type(storage, bot: Bot):
    """Юнит-тест на то, что функция возвращает корректное сообщение и
     записывает 'group_type' в контекст.
    """
    callback = AsyncMock()
    state = FSMContext(storage=storage,
                       key=StorageKey(
                           bot_id=bot.id,
                           user_id=TEST_USER.id,
                           chat_id=TEST_USER_CHAT.id))
    await process_group_type(callback=callback, state=state)
    assert await state.get_data() == {'group_type': callback.data}
    callback.message.answer.assert_called_with(text=f'Тип агрегирования выбран "{callback.data}".')


@pytest.mark.asyncio
async def test_command_type(storage, bot: Bot):
    """Юнит-тест на то, что функция возвращает корректное сообщение,
    инлайн клавиатуру и состояние ожидания 'group_type' для записи в контекст.
    """
    message = AsyncMock()
    state = FSMContext(storage=storage,
                       key=StorageKey(
                           bot_id=bot.id,
                           user_id=TEST_USER.id,
                           chat_id=TEST_USER_CHAT.id))
    await command_type(message=message, state=state)
    assert await state.get_state() == 'Query:group_type'
    message.answer.assert_called_with(text='Выберите тип группировки данных: ',
                                      reply_markup=inline_keyboard)


@pytest.mark.asyncio
async def test_command_report(storage, bot: Bot):
    """Юнит-тест на то, что функция возвращает данные из контекста
    для формирования отчёта и возвращает корректное сообщение.
    """
    message = AsyncMock()
    state = FSMContext(storage=storage,
                       key=StorageKey(
                           bot_id=bot.id,
                           user_id=TEST_USER.id,
                           chat_id=TEST_USER_CHAT.id))
    await state.update_data(dt_from=datetime(2022, 7, 25, 0, 0),
                            dt_upto=datetime(2022, 7, 27, 23, 59),
                            group_type='day')
    await command_report(message=message, state=state)
    data = await state.get_data()
    report = await get_report(data)
    message.answer.assert_called_with(text=f'Отчёт:\n{report}')

