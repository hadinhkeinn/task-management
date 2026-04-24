from typing import Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskPagination
from app.repositories.task_repository import TaskRepository

class TaskService:
    def __init__(self, db: AsyncSession):
        self.task_repo = TaskRepository(db)

    async def get_tasks(self, current_user: User, page: int = 1, limit: int = 10, status: Optional[str] = None) -> TaskPagination:
        tasks, total = await self.task_repo.get_tasks_with_count(
            user_id=current_user.id, page=page, limit=limit, status=status
        )
        
        pages = (total + limit - 1) // limit if total > 0 else 0
        
        return TaskPagination(
            items=tasks,
            total=total,
            page=page,
            limit=limit,
            pages=pages
        )

    async def create_task(self, task_in: TaskCreate, current_user: User) -> Task:
        obj_in = task_in.model_dump()
        obj_in["user_id"] = current_user.id
        return await self.task_repo.create(obj_in=obj_in)

    async def get_task(self, task_id: int, current_user: User) -> Task:
        task = await self.task_repo.get_by_id_and_user(id=task_id, user_id=current_user.id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    async def update_task(self, task_id: int, task_in: TaskUpdate, current_user: User) -> Task:
        task = await self.get_task(task_id, current_user)
        return await self.task_repo.update(db_obj=task, obj_in=task_in)

    async def delete_task(self, task_id: int, current_user: User) -> None:
        task = await self.get_task(task_id, current_user)
        await self.task_repo.delete(id=task.id)
