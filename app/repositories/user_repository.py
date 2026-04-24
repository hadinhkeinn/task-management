from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_email(self, *, email: str) -> Optional[User]:
        query = select(User).filter(User.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()
