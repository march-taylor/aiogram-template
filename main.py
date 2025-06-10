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
from middlewares.user_middleware import UserMiddleware
from features.start.handlers import router as start_router


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class I18nMiddleware:
    def __init__(self):
        self.locales = {}
        self.load_locales()
    
    def load_locales(self):
        locales_dir = Path(__file__).parent / "locales"
        for lang_file in locales_dir.glob("*.json"):
            with open(lang_file, 'r', encoding='utf-8') as f:
                self.locales[lang_file.stem] = json.load(f)

    async def get_user_locale(self, user: Any) -> str:
        from database.users import UserRepository
        user_repo = UserRepository()
        db_user = await user_repo.get_user(user.id)
        return db_user['language'] if db_user else Config.DEFAULT_LANGUAGE
    
    def gettext(self, key: str, locale: str = None, **kwargs) -> str:
        locale = locale or Config.DEFAULT_LANGUAGE
        text = self.locales.get(locale, {}).get(key, key)
        return text.format(**kwargs) if kwargs else text

async def setup_database():
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    await setup_database()
    
    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Инициализация локализации
    i18n = I18nMiddleware()
    
    # Регистрация middleware
    dp.message.middleware(UserMiddleware(i18n))
    dp.callback_query.middleware(UserMiddleware(i18n))
    
    # Регистрация роутеров
    dp.include_router(start_router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())