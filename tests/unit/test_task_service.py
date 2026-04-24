import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.task import TaskCreate, TaskUpdate
from app.services.task_service import TaskService
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate
import pytest_asyncio

@pytest_asyncio.fixture
async def mock_user(db_session: AsyncSession):
    service = AuthService(db_session)
    return await service.register(UserCreate(email="taskuser1@example.com", password="password123"))

@pytest_asyncio.fixture
async def mock_other_user(db_session: AsyncSession):
    service = AuthService(db_session)
    return await service.register(UserCreate(email="otheruser@example.com", password="password123"))

@pytest.mark.asyncio
async def test_create_and_get_task(db_session: AsyncSession, mock_user):
    task_service = TaskService(db_session)
    task_in = TaskCreate(title="Test Task", status="todo")
    
    # Create task
    task = await task_service.create_task(task_in, mock_user)
    assert task.id is not None
    assert task.title == "Test Task"
    assert task.user_id == mock_user.id
    assert task.status == "todo"
    
    # Get task ownership
    task_get = await task_service.get_task(task.id, mock_user)
    assert task_get.id == task.id

@pytest.mark.asyncio
async def test_task_ownership_check(db_session: AsyncSession, mock_user, mock_other_user):
    task_service = TaskService(db_session)
    task_in = TaskCreate(title="User1 Task", status="todo")
    task = await task_service.create_task(task_in, mock_user)
    
    # Other user trying to get, update, or delete should raise 404
    with pytest.raises(HTTPException) as exc_info:
        await task_service.get_task(task.id, mock_other_user)
    assert exc_info.value.status_code == 404
    
    with pytest.raises(HTTPException) as exc_info:
        await task_service.update_task(task.id, TaskUpdate(title="updated"), mock_other_user)
    assert exc_info.value.status_code == 404
    
    with pytest.raises(HTTPException) as exc_info:
        await task_service.delete_task(task.id, mock_other_user)
    assert exc_info.value.status_code == 404

@pytest.mark.asyncio
async def test_pagination_math(db_session: AsyncSession, mock_user):
    task_service = TaskService(db_session)
    
    # Create 15 tasks
    for i in range(15):
        await task_service.create_task(TaskCreate(title=f"Task {i}"), mock_user)
        
    page1 = await task_service.get_tasks(mock_user, page=1, limit=10)
    assert len(page1.items) == 10
    assert page1.total == 15
    assert page1.pages == 2
    
    page2 = await task_service.get_tasks(mock_user, page=2, limit=10)
    assert len(page2.items) == 5
    assert page2.total == 15
    assert page2.pages == 2
