import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_full_tasks_crud_flow(async_client: AsyncClient, auth_headers):
    # 1. Create a task
    res = await async_client.post("/api/v1/tasks", json={"title": "Test Task", "status": "todo"}, headers=auth_headers)
    assert res.status_code == 201
    task = res.json()
    assert task["title"] == "Test Task"
    task_id = task["id"]
    
    # 2. Get the task
    res = await async_client.get("/api/v1/tasks", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 1
    assert any(t["id"] == task_id for t in data["items"])
    
    # 3. Update the task
    res = await async_client.put(f"/api/v1/tasks/{task_id}", json={"title": "Updated Task", "status": "doing"}, headers=auth_headers)
    assert res.status_code == 200
    updated_task = res.json()
    assert updated_task["title"] == "Updated Task"
    assert updated_task["status"] == "doing"
    
    # 4. Delete the task
    res = await async_client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert res.status_code == 204
    
    # 5. Verify deletion
    res = await async_client.get("/api/v1/tasks", headers=auth_headers)
    data = res.json()
    assert not any(t["id"] == task_id for t in data["items"])

@pytest.mark.asyncio
async def test_user_separation(async_client: AsyncClient, test_user, auth_headers, admin_headers):
    # test_user creates a task
    res = await async_client.post("/api/v1/tasks", json={"title": "User A Task"}, headers=auth_headers)
    assert res.status_code == 201
    task_id = res.json()["id"]
    
    # admin_user tries to get/edit/delete it via regular tasks endpoint (should fail, only their own tasks)
    res = await async_client.put(f"/api/v1/tasks/{task_id}", json={"title": "Hacked"}, headers=admin_headers)
    assert res.status_code == 404
    
    res = await async_client.delete(f"/api/v1/tasks/{task_id}", headers=admin_headers)
    assert res.status_code == 404

    # admin_headers does not show the task
    res = await async_client.get("/api/v1/tasks", headers=admin_headers)
    assert res.status_code == 200
    assert not any(t["id"] == task_id for t in res.json()["items"])

@pytest.mark.asyncio
async def test_pagination(async_client: AsyncClient, auth_headers):
    for i in range(15):
        await async_client.post("/api/v1/tasks", json={"title": f"T{i}"}, headers=auth_headers)
        
    res = await async_client.get("/api/v1/tasks?page=1&limit=10", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) == 10
    
    res = await async_client.get("/api/v1/tasks?page=2&limit=10", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) == 5

