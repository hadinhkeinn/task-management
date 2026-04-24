from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut, UserLogin
from app.schemas.auth import Token, RefreshTokenRequest
from app.services.auth_service import AuthService
from app.core.rate_limit import limiter

router = APIRouter()

def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)

@router.post("/register", response_model=UserOut, status_code=201)
@limiter.limit("5/minute")
async def register(request: Request, user_in: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.register(user_in)

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(request: Request, user_credentials: UserLogin, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.login(user_credentials.email, user_credentials.password)

@router.post("/refresh", response_model=Token)
async def refresh(req: RefreshTokenRequest, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.refresh(req)
