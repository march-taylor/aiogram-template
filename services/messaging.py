from aiogram import Bot
from typing import Awaitable, Callable

from services.language import LanguageService
from middlewares.i18n import i18n

class MessagingService:
	_bot_instance: Bot | None = None

	@classmethod
	def setup(cls, bot: Bot) -> None:
		"""Инициализация бота перед использованием."""
		cls._bot_instance = bot

	@staticmethod
	async def send_localized(
		user_id: int,
		message_key: str,
		**format_kwargs
	) -> None:
		if MessagingService._bot_instance is None:
			raise RuntimeError("Bot instance not initialized. Call MessagingService.setup(bot) first.")
		
		bot = MessagingService._bot_instance
		language = await LanguageService.get_user_language(user_id)
		text = i18n.get_text(key=message_key, locale=language)
		
		if format_kwargs:
			text = text.format(**format_kwargs)
		
		await bot.send_message(user_id, text)