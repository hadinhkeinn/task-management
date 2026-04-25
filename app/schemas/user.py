from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserLogin(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    role: str | None = None
    password: str | None = Field(None, min_length=8)

class UserOut(UserBase):
    id: int
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserPagination(BaseModel):
    items: list[UserOut]
    total: int
    page: int
    limit: int
    pages: int
