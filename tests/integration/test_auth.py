import pytest
from httpx import AsyncClient
import pytest_asyncio

@pytest.mark.asyncio
async def test_register_login_refresh_cycle(async_client: AsyncClient):
    # Register
    res = await async_client.post(
        "/api/v1/auth/register",
        json={"email": "cycle@example.com", "password": "password123"}
    )
    assert res.status_code == 201
    
    # Login
    res = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "cycle@example.com", "password": "password123"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert "refresh_token" in data
    
    refresh_token = data["refresh_token"]
    
    # Refresh
    res = await async_client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert "refresh_token" in data

@pytest.mark.asyncio
async def test_rate_limit(async_client: AsyncClient):
    # Spam 6 logins to trip slowapi rate limit (5/minute)
    headers = {"X-Forwarded-For": "1.2.3.4"}
    hit_rate_limit = False
    for _ in range(6):
        res = await async_client.post(
            "/api/v1/auth/login",
            json={"email": "nonexistent@example.com", "password": "pwd"},
            headers=headers
        )
        if res.status_code == 429:
            hit_rate_limit = True
            break
        assert res.status_code in [401, 200]
        
    assert hit_rate_limit, "Did not hit rate limit"
