import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import load_config
from bot.handlers.command_handlers import command_router
from bot.handlers.text_handlers import text_router, formatted_router


async def main() -> None:
    config = load_config()

    # Инициализация хранилища
    storage = MemoryStorage()

    # Создание объектов бота и диспетчера
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)

    # Регистрация роутеров в диспетчере
    dp.include_routers(command_router, formatted_router, text_router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

