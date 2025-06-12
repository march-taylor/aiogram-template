import json
from pathlib import Path
from typing import Any
from aiogram import BaseMiddleware
from config import Config

class I18nMiddleware(BaseMiddleware):
	def __init__(self):
		super().__init__()
		self.locales = {}
		self.load_locales()
	
	def load_locales(self):
		locales_dir = Path(__file__).parent.parent / "locales"
		for lang_file in locales_dir.glob("*.json"):
			with open(lang_file, 'r', encoding='utf-8') as f:
				self.locales[lang_file.stem] = json.load(f)

	async def get_user_locale(self, user_id: int) -> str:
		from database.users import UserRepository
		user_repo = UserRepository()
		db_user = await user_repo.get_user(user_id)
		return db_user['language'] if db_user else Config.DEFAULT_LANGUAGE
	
	def get_text(self, key: str, locale: str = None, **kwargs) -> str:
		locale = locale or Config.DEFAULT_LANGUAGE
		text = self.locales.get(locale, {}).get(key, key)
		return text.format(**kwargs) if kwargs else text

	async def __call__(self, handler, event, data):
		if not hasattr(event, "from_user") or not event.from_user:
			return await handler(event, data)

		user_id = event.from_user.id
		locale = await self.get_user_locale(user_id)

		data["_"] = lambda key, **kwargs: self.get_text(key, locale=locale, **kwargs)
		return await handler(event, data)

i18n = I18nMiddleware()