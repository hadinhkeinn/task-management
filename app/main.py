from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.api.v1.router import api_router_v1
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.rate_limit import limiter
from app.core.swagger import get_custom_swagger_html
from app.middleware.logging_middleware import LoggingMiddleware

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="REST API with JWT auth and role-based access",
    docs_url=None,
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

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_custom_swagger_html(
        openapi_url="/openapi.json",
        title=settings.PROJECT_NAME,
    )

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        description="REST API with JWT auth and role-based access",
        routes=app.routes,
        tags=[
            {"name": "auth", "description": "Register, login, token refresh"},
            {"name": "users", "description": "Current user info"},
            {"name": "tasks", "description": "Task CRUD"},
            {"name": "admin", "description": "Admin-only operations"},
        ]
    )

    schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
        }
    }

    excluded = {"/api/v1/auth/login", "/api/v1/auth/register", "/api/v1/auth/refresh", "/health"}
    for path, methods in schema.get("paths", {}).items():
        if path not in excluded:
            for operation in methods.values():
                operation.setdefault("security", [{"HTTPBearer": []}])

    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi
@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}

