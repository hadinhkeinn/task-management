from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.api.v1.router import api_router_v1
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.rate_limit import limiter
from app.middleware.logging_middleware import LoggingMiddleware

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="REST API with JWT auth and role-based access",
    openapi_tags=[
        {"name": "auth", "description": "Register, login, token refresh"},
        {"name": "users", "description": "Current user info"},
        {"name": "tasks", "description": "Task CRUD"},
        {"name": "admin", "description": "Admin-only operations"},
    ]
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(LoggingMiddleware)

app.include_router(api_router_v1, prefix="/api/v1")

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}

