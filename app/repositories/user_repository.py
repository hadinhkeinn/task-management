from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.user import User
from app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_users_with_count(
        self, page: int, limit: int
    ) -> tuple[list[User], int]:
        query = select(User)
        total_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(total_query) or 0

        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)

        result = await self.db.execute(query)
        users = list(result.scalars().all())

        return users, total

    async def get_by_email(self, *, email: str) -> Optional[User]:
        query = select(User).filter(User.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()
