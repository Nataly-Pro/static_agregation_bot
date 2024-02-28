import pytest
from aiogram import Dispatcher, Bot
from aiogram.methods import SendMessage
from aiogram3_calendar import DialogCalendar

from tests.test_handlers.utils import get_message, get_update


@pytest.mark.asyncio
async def test_command_date(dispatcher: Dispatcher, bot: Bot):
    result = await dispatcher.feed_update(
        bot=bot,
        update=get_update(message=get_message(text='/date_from'))
    )
    assert isinstance(result, SendMessage)
    assert result.text == 'Выберите дату начала периода:'
    assert result.reply_markup == await DialogCalendar().start_calendar()


