from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal, Optional


class TaskBase(BaseModel):
    title: str = Field(..., max_length=500, min_length=1)
    status: Literal["todo", "doing", "done"] = "todo"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=500, min_length=1)
    status: Optional[Literal["todo", "doing", "done"]] = None


class TaskOut(TaskBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TaskPagination(BaseModel):
    items: list[TaskOut]
    total: int
    page: int
    limit: int
    pages: int

