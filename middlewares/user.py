# middlewares/user_middleware.py
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from typing import Callable, Awaitable, Any, Dict, Union


class UserMiddleware(BaseMiddleware):
	def __init__(self):
		pass
	
	async def __call__(
		self,
		handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
		event: Union[Message, CallbackQuery],
		data: Dict[str, Any]
	) -> Any:
		user = None
		
		if hasattr(event, "from_user") and event.from_user:
			from database.users import UserRepository
			user_repo = UserRepository()
			user = await user_repo.get_user(event.from_user.id)
		
		data["user"] = user
		
		return await handler(event, data)