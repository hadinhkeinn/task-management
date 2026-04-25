from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserOut, UserUpdate, UserPagination
from app.schemas.task import TaskOut, TaskUpdate, TaskPagination
from app.services.admin_service import AdminService

router = APIRouter()

def get_admin_service(db: AsyncSession = Depends(get_db)) -> AdminService:
    return AdminService(db)

# --- USER MANAGEMENT ---
@router.get("/users", response_model=UserPagination)
async def get_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    admin_service: AdminService = Depends(get_admin_service),
):
    return await admin_service.get_users(page, limit)

@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int,
    admin_service: AdminService = Depends(get_admin_service),
):
    return await admin_service.get_user(user_id)

@router.put("/users/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    admin_service: AdminService = Depends(get_admin_service),
):
    return await admin_service.update_user(user_id, user_in)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    admin_service: AdminService = Depends(get_admin_service),
):
    await admin_service.delete_user(user_id)

# --- TASK MANAGEMENT ---
@router.get("/tasks", response_model=TaskPagination)
async def get_all_tasks(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    admin_service: AdminService = Depends(get_admin_service),
):
    return await admin_service.get_all_tasks(page, limit, status)

@router.get("/tasks/{task_id}", response_model=TaskOut)
async def get_task(
    task_id: int,
    admin_service: AdminService = Depends(get_admin_service),
):
    return await admin_service.get_task(task_id)

@router.put("/tasks/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: int,
    task_in: TaskUpdate,
    admin_service: AdminService = Depends(get_admin_service),
):
    return await admin_service.update_task(task_id, task_in)

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    admin_service: AdminService = Depends(get_admin_service),
):
    await admin_service.delete_task(task_id)
