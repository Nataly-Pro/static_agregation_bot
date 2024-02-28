import asyncio
from aiogram import Bot, Dispatcher

from bot.config import load_config
from bot.handlers.command_handlers import command_router
from bot.handlers.text_handlers import text_router, formatted_router


async def main() -> None:
    config = load_config()
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    # Регистрируем роутер в диспетчере
    dp.include_router(command_router)
    dp.include_router(formatted_router)
    dp.include_router(text_router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

