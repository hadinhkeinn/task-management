import pytest
from httpx import AsyncClient
from app.core.security import create_access_token

@pytest.mark.asyncio
async def test_get_me_valid_token(async_client: AsyncClient, test_user, auth_headers):
    res = await async_client.get("/api/v1/users/me", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == test_user.email
    assert data["role"] == "user"

@pytest.mark.asyncio
async def test_get_me_invalid_token(async_client: AsyncClient):
    res = await async_client.get("/api/v1/users/me", headers={"Authorization": "Bearer badtoken"})
    assert res.status_code == 401

@pytest.mark.asyncio
async def test_get_me_expired_token(async_client: AsyncClient, test_user):
    from datetime import timedelta
    token = create_access_token(data={"sub": str(test_user.id), "role": test_user.role}, expires_delta=timedelta(minutes=-10))
    res = await async_client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 401

