from database.users import UserRepository


class LanguageService:
	@staticmethod
	async def set_user_language(user_id: int, language_code: str) -> None:
		repo = UserRepository()
		await repo.add_user(user_id, language_code)

	@staticmethod
	async def get_user_language(user_id: int) -> str:
		repo = UserRepository()
		user = await repo.get_user(user_id)
		return user['language'] if user else "en"