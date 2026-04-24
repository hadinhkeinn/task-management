from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut, TaskPagination
from app.services.task_service import TaskService

router = APIRouter()

def get_task_service(db: AsyncSession = Depends(get_db)) -> TaskService:
    return TaskService(db)

@router.get("", response_model=TaskPagination)
async def get_tasks(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    task_service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user)
):
    return await task_service.get_tasks(current_user, page, limit, status)

@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    task_service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user)
):
    return await task_service.create_task(task_in, current_user)

@router.put("/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: int,
    task_in: TaskUpdate,
    task_service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user)
):
    return await task_service.update_task(task_id, task_in, current_user)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user)
):
    await task_service.delete_task(task_id, current_user)
