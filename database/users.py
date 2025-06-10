from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import db
from database.setup import User


class UserRepository:
    async def add_user(self, user_id: int, language: str = "en") -> dict:
        async with db.session() as session:
            user = User(user_id=user_id, language=language)
            session.add(user)
            await session.flush()
            return {"user_id": user.user_id, "language": user.language}

    async def get_user(self, user_id: int) -> dict | None:
        async with db.session() as session:
            result = await session.execute(select(User).where(User.user_id == user_id))
            user = result.scalar_one_or_none()
            return {
                "user_id": user.user_id,
                "language": user.language,
                "added_at": user.added_at
            } if user else None

    async def update_language(self, user_id: int, language: str) -> dict:
        async with db.session() as session:
            await session.execute(
                update(User)
                .where(User.user_id == user_id)
                .values(language=language)
            )
            return {"user_id": user_id, "language": language}