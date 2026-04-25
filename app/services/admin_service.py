from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.task import Task
from app.schemas.user import UserUpdate, UserPagination
from app.schemas.task import TaskUpdate, TaskPagination
from app.repositories.user_repository import UserRepository
from app.repositories.task_repository import TaskRepository
from app.core.security import hash_password
class AdminService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.task_repo = TaskRepository(db)
    # Users
    async def get_users(self, page: int = 1, limit: int = 10) -> UserPagination:
        users, total = await self.user_repo.get_users_with_count(page=page, limit=limit)
        pages = (total + limit - 1) // limit if total > 0 else 0
        return UserPagination(
            items=users,
            total=total,
            page=page,
            limit=limit,
            pages=pages
        )

    async def get_user(self, user_id: int) -> User:
        user = await self.user_repo.get(id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def update_user(self, user_id: int, user_in: UserUpdate) -> User:
        user = await self.get_user(user_id)
        update_data = user_in.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["password"] = hash_password(update_data["password"])
        # ensure email uniqueness if changed
        if "email" in update_data and update_data["email"] != user.email:
            existing = await self.user_repo.get_by_email(email=update_data["email"])
            if existing:
                raise HTTPException(status_code=400, detail="Email already registered")
        return await self.user_repo.update(db_obj=user, obj_in=update_data)

    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user(user_id)
        await self.user_repo.delete(id=user.id)

    # Tasks
    async def get_all_tasks(self, page: int = 1, limit: int = 10, task_status: Optional[str] = None) -> TaskPagination:
        tasks, total = await self.task_repo.get_all_tasks_with_count(page=page, limit=limit, status=task_status)
        pages = (total + limit - 1) // limit if total > 0 else 0
        return TaskPagination(
            items=tasks,
            total=total,
            page=page,
            limit=limit,
            pages=pages
        )

    async def get_task(self, task_id: int) -> Task:
        task = await self.task_repo.get(id=task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    async def update_task(self, task_id: int, task_in: TaskUpdate) -> Task:
        task = await self.get_task(task_id)
        return await self.task_repo.update(db_obj=task, obj_in=task_in)

    async def delete_task(self, task_id: int) -> None:
        task = await self.get_task(task_id)
        await self.task_repo.delete(id=task.id)
