from aiogram_i18n import I18nContext
from database.users import UserRepository


class StartService:
    def __init__(self):
        self.user_repo = UserRepository()

    async def register_user(self, user_id: int, i18n: I18nContext) -> dict:
        user = await self.user_repo.get_user(user_id)
        if not user:
            user = await self.user_repo.add_user(user_id, i18n.locale)
        return user

    async def set_language(self, user_id: int, language: str) -> dict:
        return await self.user_repo.update_language(user_id, language)