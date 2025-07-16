import asyncio
from handlers import register_handlers
from middlewares.db_session_middleware import DBSessionMiddleware
from create_bot import *
from database.db import init_db
from services.logger import log
from config import get_settings

settings = get_settings()


async def on_startup():
    log.info("Initializing database...")
    await init_db()
    log.info("Database initialized successfully")
    # Start parsing gifts
    log.info("Starting gift parsing loop...")
    for admin in settings.bot.admins:
        try:
            await bot.send_message(admin, 'Бот запущен!')
        except Exception:
            pass


async def main():
    log.info("Starting bot...")

    await on_startup()

    dp.update.middleware(DBSessionMiddleware())

    # Register handlers
    register_handlers(dp)

    # Start polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
