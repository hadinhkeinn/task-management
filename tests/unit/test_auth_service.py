import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate
from app.services.auth_service import AuthService

@pytest.mark.asyncio
async def test_register_duplicate_email_raises(db_session: AsyncSession):
    auth_service = AuthService(db_session)
    user_in = UserCreate(email="duplicate@example.com", password="password123")
    
    # Register first time
    await auth_service.register(user_in)
    
    # Register second time
    with pytest.raises(HTTPException) as exc_info:
        await auth_service.register(user_in)
        
    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Email already registered"

@pytest.mark.asyncio
async def test_login_wrong_password_raises(db_session: AsyncSession):
    auth_service = AuthService(db_session)
    user_in = UserCreate(email="login@example.com", password="password123")
    await auth_service.register(user_in)
    
    with pytest.raises(HTTPException) as exc_info:
        await auth_service.login(email="login@example.com", password="wrongpassword")
        
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Incorrect email or password"

