import asyncio
import json
from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import User
from typing import Any, Dict
import logging

from config import Config
from database.database import db
from database.setup import Base
from middlewares.user import UserMiddleware
from middlewares.i18n import I18nMiddleware
from features.start.handlers import router as start_router


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def setup_database():
	async with db.engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)

async def main():
	await setup_database()
	
	bot = Bot(token=Config.BOT_TOKEN)
	dp = Dispatcher(storage=MemoryStorage())
	
	# Инициализация middleware
	i18n_middleware = I18nMiddleware()
	user_middleware = UserMiddleware()
	
	# Регистрация middleware
	dp.message.outer_middleware.register(i18n_middleware)
	dp.message.outer_middleware.register(user_middleware)
	dp.callback_query.outer_middleware.register(i18n_middleware)
	dp.callback_query.outer_middleware.register(user_middleware)
	
	# Регистрация роутеров
	dp.include_router(start_router)
	
	await dp.start_polling(bot)

if __name__ == "__main__":
	asyncio.run(main())