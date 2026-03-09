import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from DB.database import session, init_db
from bot.handlers import start, admin, program
from bot.middlewares.DB import DbSessionMiddleware
from config import CONFIG

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    await init_db()
    # Инициализация бота и диспетчера
    bot = Bot(
        token=CONFIG['BOT_TOKEN'],
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация middleware
    dp.update.middleware(DbSessionMiddleware(session))

    # Регистрация роутеров (хендлеров)
    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(program.router)

    # Запуск
    try:
        logger.info("Starting bot...")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await dp.storage.close()


if __name__ == "__main__":
    asyncio.run(main())
