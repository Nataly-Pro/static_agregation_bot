import pytest
from aiogram import Dispatcher, Bot
from aiogram.methods import SendMessage
from aiogram3_calendar import DialogCalendar

from bot.keyboards import inline_keyboard
from bot.lexicon import LEXICON
from tests.test_handlers.utils import get_update, get_message


@pytest.mark.asyncio
async def test_process_text(dispatcher: Dispatcher, bot: Bot):
    """Интеграционный тест на то, какой хэндлер перехватит
    входящий запрос с форматированным текстовым сообщением.
    """
    valid_formatted_text = '{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-10-31T23:59:00", "group_type": "month"}'
    valid_some_text = 'Необходимо посчитать суммы всех выплат с 1 февраля 2022 по 31 марта 2022, ' \
                      'единица группировки - месяц.'
    invalid_text = 'Тест'

    result = await dispatcher.feed_update(
        bot=bot,
        update=get_update(message=get_message(text=valid_formatted_text))
    )
    assert result.text == "Отчёт:\n{'dataset': [5906586, 5515874], " \
                          "'labels': ['2022-09-01T00:00:00', '2022-10-01T00:00:00']}"

    result = await dispatcher.feed_update(
        bot=bot,
        update=get_update(message=get_message(text=valid_some_text))
    )
    assert result.text == ('Отчёт:\n'
                           "{'dataset': [5466335, 6154530], 'labels': ['2022-02-01T00:00:00', "
                           "'2022-03-01T00:00:00']}")

    error_result = await dispatcher.feed_update(
        bot=bot,
        update=get_update(message=get_message(text=invalid_text))
    )
    assert error_result.text == LEXICON['error']


@pytest.mark.asyncio
async def test_command_date(dispatcher: Dispatcher, bot: Bot):
    """Интеграционный тест на то, какой хэндлер перехватит
    входящий запрос с сообщениями '/date_from', '/date_to'
    и '/group_type'.
    """
    # для '/date_from'
    result = await dispatcher.feed_update(
        bot=bot,
        update=get_update(message=get_message(text='/date_from'))
    )
    assert isinstance(result, SendMessage)
    assert result.text == 'Выберите дату начала периода:'
    assert result.reply_markup == await DialogCalendar().start_calendar()

    # для '/date_to'
    result = await dispatcher.feed_update(
        bot=bot,
        update=get_update(message=get_message(text='/date_to'))
    )
    assert result.text == 'Выберите дату окончания периода:'
    assert result.reply_markup == await DialogCalendar().start_calendar()

    # для '/group_type'
    result = await dispatcher.feed_update(
        bot=bot,
        update=get_update(message=get_message(text='/group_type'))
    )
    assert result.text == 'Выберите тип группировки данных: '
    assert result.reply_markup == inline_keyboard