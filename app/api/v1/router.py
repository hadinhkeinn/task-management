from fastapi import APIRouter, Depends
from app.api.v1.endpoints import auth, users, tasks, admin
from app.api.deps import get_current_admin

api_router_v1 = APIRouter()
api_router_v1.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router_v1.include_router(users.router, prefix="/users", tags=["users"])
api_router_v1.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router_v1.include_router(admin.router, prefix="/admin", tags=["admin"], dependencies=[Depends(get_current_admin)])
