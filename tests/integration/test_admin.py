import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestAdminEndpoints:
    
    async def test_get_users_unauthorized(self, async_client: AsyncClient, auth_headers):
        # A normal user should not be able to access admin endpoints
        response = await async_client.get("/api/v1/admin/users", headers=auth_headers)
        assert response.status_code == 403

    async def test_get_users_authorized(self, async_client: AsyncClient, admin_headers, test_user):
        response = await async_client.get("/api/v1/admin/users", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] >= 2  # Including admin_user and test_user

    async def test_get_single_user(self, async_client: AsyncClient, admin_headers, test_user):
        response = await async_client.get(f"/api/v1/admin/users/{test_user.id}", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["id"] == test_user.id

    async def test_update_user_role(self, async_client: AsyncClient, admin_headers, test_user):
        update_data = {"role": "admin"}
        response = await async_client.put(f"/api/v1/admin/users/{test_user.id}", json=update_data, headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["role"] == "admin"

    async def test_delete_user(self, async_client: AsyncClient, admin_headers, test_user):
        response = await async_client.delete(f"/api/v1/admin/users/{test_user.id}", headers=admin_headers)
        assert response.status_code == 204
        
        # Verify user is deleted
        check_res = await async_client.get(f"/api/v1/admin/users/{test_user.id}", headers=admin_headers)
        assert check_res.status_code == 404

    async def test_get_all_tasks(self, async_client: AsyncClient, admin_headers, test_user, auth_headers):
        # First create a task using normal user
        task_data = {
            "title": "Normal User Task",
            "status": "todo",
        }
        create_res = await async_client.post("/api/v1/tasks", json=task_data, headers=auth_headers)
        assert create_res.status_code == 201
        
        # Now admin fetches all tasks
        response = await async_client.get("/api/v1/admin/tasks", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) >= 1
        assert data["items"][0]["title"] == "Normal User Task"

    async def test_admin_update_task(self, async_client: AsyncClient, admin_headers, test_user, auth_headers):
        # First create a task using normal user
        task_data = {
            "title": "To be evaluated",
            "status": "todo",
        }
        create_res = await async_client.post("/api/v1/tasks", json=task_data, headers=auth_headers)
        task_id = create_res.json()["id"]

        # Admin updates the task
        update_data = {
            "status": "doing",
        }
        res = await async_client.put(f"/api/v1/admin/tasks/{task_id}", json=update_data, headers=admin_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "doing"

    async def test_admin_delete_task(self, async_client: AsyncClient, admin_headers, test_user, auth_headers):
        # Normal user creates task
        task_data = {"title": "Will be deleted", "status": "todo"}
        create_res = await async_client.post("/api/v1/tasks", json=task_data, headers=auth_headers)
        task_id = create_res.json()["id"]

        # Admin deletes task
        del_res = await async_client.delete(f"/api/v1/admin/tasks/{task_id}", headers=admin_headers)
        assert del_res.status_code == 204

        # Verify deletion
        get_res = await async_client.get(f"/api/v1/admin/tasks/{task_id}", headers=admin_headers)
        assert get_res.status_code == 404

