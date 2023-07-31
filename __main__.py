import asyncio
import logging
import sys
import time

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.notification_handler import time_for_push
from sqlalchemy.ext.asyncio import (async_sessionmaker,
                                    create_async_engine)

import config
import handlers.change_mode_handler
import handlers.change_push_mode_handler
import handlers.change_time_handler
import handlers.get_history_handler
import handlers.menu_handler
import handlers.set_record_handler
import handlers.start_handler
from config import DB_URL
from middlewares.db import DbSessionMiddleware

TOKEN = config.TOKEN


def check_token():
    """checking telegram token"""
    return TOKEN


async def main():
    engine = create_async_engine(url=DB_URL, echo=True)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)

    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(DbSessionMiddleware(session_pool=async_session_maker))

    dp.include_router(handlers.start_handler.router)
    dp.include_router(handlers.get_history_handler.router)
    dp.include_router(handlers.change_mode_handler.router)
    dp.include_router(handlers.change_time_handler.router)
    dp.include_router(handlers.change_push_mode_handler.router)
    dp.include_router(handlers.set_record_handler.router)
    dp.include_router(handlers.menu_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    while True:
        await time_for_push()
        time.sleep(60)


if __name__ == "__main__":
    if not check_token():
        logging.critical('Check Token in .env')
        sys.exit('Check Token in .env')
    asyncio.run(main())
