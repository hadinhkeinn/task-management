from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.auth import Token, RefreshTokenRequest
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.config import settings
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from datetime import datetime, timezone, timedelta

class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.token_repo = RefreshTokenRepository(db)

    async def register(self, user_in: UserCreate) -> User:
        user = await self.user_repo.get_by_email(email=user_in.email)
        if user:
            raise HTTPException(status_code=409, detail="Email already registered")
        
        user_data = {
            "email": user_in.email,
            "password": hash_password(user_in.password),
            "role": "user"
        }
        return await self.user_repo.create(obj_in=user_data)

    async def login(self, email: str, password: str) -> Token:
        user = await self.user_repo.get_by_email(email=email)
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        
        access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        await self.token_repo.create(obj_in={
            "token": refresh_token,
            "user_id": user.id,
            "expires_at": expires_at
        })
        
        return Token(access_token=access_token, refresh_token=refresh_token)

    async def refresh(self, req: RefreshTokenRequest) -> Token:
        payload = decode_token(req.refresh_token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid refresh token format or expired completely")
            
        stored_token = await self.token_repo.get_by_token(token=req.refresh_token)
        if not stored_token:
            raise HTTPException(status_code=401, detail="Refresh token not found or revoked")
            
        if stored_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            await self.token_repo.delete(id=stored_token.id)
            raise HTTPException(status_code=401, detail="Refresh token expired")
            
        user_id = payload.get("sub")
        user = await self.user_repo.get(id=int(user_id))
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
        new_refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        await self.token_repo.delete(id=stored_token.id)
        
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        await self.token_repo.create(obj_in={
            "token": new_refresh_token,
            "user_id": user.id,
            "expires_at": expires_at
        })
        
        return Token(access_token=access_token, refresh_token=new_refresh_token)
