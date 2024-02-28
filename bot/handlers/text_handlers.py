from aiogram import Router, Bot, F
from aiogram.types import Message
from bot.config import load_config
from bot.lexicon import LEXICON
from bot.services import get_report, get_data_from_text

config = load_config()
bot = Bot(token=config.tg_bot.token)
text_router = Router()
formatted_router = Router()


@formatted_router.message(F.text.startswith('{'))
async def process_formatted_text(message: Message):
    """Этот хэндлер будет срабатывать на текстовые сообщения,
    имитирующие json формат.
    """
    data = message.text
    return await bot.send_message(message.from_user.id, f'Отчёт:\n{await get_report(data)}')


@text_router.message()
async def process_some_text(message: Message):
    """Этот хэндлер будет срабатывать на любые сообщения,
    кроме зарезервированных команд.
    """
    try:
        data = await get_data_from_text(message.text)
        await bot.send_message(message.from_user.id, f'Отчёт:\n{await get_report(data)}')
    except (AttributeError, IndexError):
        await message.answer(text=LEXICON['error'])
