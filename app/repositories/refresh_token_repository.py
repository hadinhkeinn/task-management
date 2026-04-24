from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.refresh_token import RefreshToken
from app.repositories.base_repository import BaseRepository

class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self, db: AsyncSession):
        super().__init__(RefreshToken, db)

    async def get_by_token(self, *, token: str) -> Optional[RefreshToken]:
        query = select(RefreshToken).filter(RefreshToken.token == token)
        result = await self.db.execute(query)
        return result.scalars().first()

