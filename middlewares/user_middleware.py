from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from typing import Callable, Awaitable, Any, Dict, Union


class UserMiddleware(BaseMiddleware):
	def __init__(self, i18n):
		self.i18n = i18n
	
	async def __call__(
		self,
		handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
		event: Union[Message, CallbackQuery],
		data: Dict[str, Any]
	) -> Any:
		user = None
		
		# Получение пользователя в зависимости от типа события
		if isinstance(event, Message):
			user = event.from_user
		elif isinstance(event, CallbackQuery):
			user = event.from_user
		
		if user:
			from database.users import UserRepository
			user_repo = UserRepository()
			
			db_user = await user_repo.get_user(user.id)
			if not db_user:
				db_user = await user_repo.add_user(
					user.id, 
					await self.i18n.get_user_locale(user)
				)
			
			data["user"] = db_user
			data["i18n"] = self.i18n
		
		return await handler(event, data)