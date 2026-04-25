from typing import Optional, Tuple, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.task import Task
from app.repositories.base_repository import BaseRepository

class TaskRepository(BaseRepository[Task]):
    def __init__(self, db: AsyncSession):
        super().__init__(Task, db)

    async def get_tasks_with_count(
        self, user_id: int, page: int, limit: int, status: Optional[str] = None
    ) -> Tuple[List[Task], int]:
        query = select(Task).filter(Task.user_id == user_id)
        if status:
            query = query.filter(Task.status == status)
            
        total_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(total_query) or 0
        
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)
        
        result = await self.db.execute(query)
        tasks = list(result.scalars().all())
        
        return tasks, total

    async def get_all_tasks_with_count(
        self, page: int, limit: int, status: Optional[str] = None
    ) -> Tuple[List[Task], int]:
        query = select(Task)
        if status:
            query = query.filter(Task.status == status)
            
        total_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(total_query) or 0
        
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)
        
        result = await self.db.execute(query)
        tasks = list(result.scalars().all())
        
        return tasks, total

    async def get_by_id_and_user(self, *, id: int, user_id: int) -> Optional[Task]:
        query = select(Task).filter(Task.id == id, Task.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().first()
