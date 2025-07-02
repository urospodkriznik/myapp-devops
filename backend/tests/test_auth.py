import pytest
from httpx import AsyncClient
from starlette.testclient import TestClient
from app.main import app
from app.models import RoleEnum


@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    res = await client.post("/register", json={
        "name": "test",
        "email": "test@example.com",
        "password": "secret"
    })
    assert res.status_code == 200
    assert res.json()["email"] == "test@example.com"

    res = await client.post("/login", json={
        "email": "test@example.com",
        "password": "secret"
    })
    assert res.status_code == 200
    token = res.json()["access_token"]
    assert token

    res = await client.get("/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert res.status_code == 200
    assert res.json()["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_get_users(client: AsyncClient):
    await client.post("/register", json={
        "name": "admin",
        "email": "admin@example.com",
        "password": "secret",
        "role": RoleEnum.ADMIN.value
    })
    login_res = await client.post("/login", json={
        "email": "admin@example.com",
        "password": "secret"
    })
    token = login_res.json()["access_token"]

    res = await client.get("/users", headers={
        "Authorization": f"Bearer {token}"
    })
    assert res.status_code == 200
    users = res.json()
    assert isinstance(users, list)
    assert any(u["email"] == "admin@example.com" for u in users)


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient):
    res = await client.post("/register", json={
        "name": "delete_me",
        "email": "deleteme@example.com",
        "password": "secret"
    })
    user_id = res.json()["id"]
    res = await client.delete(f"/users/{user_id}")
    assert res.status_code == 200
    assert res.json()["ok"] is True


@pytest.mark.asyncio
async def test_get_items_empty(client: AsyncClient):
    res = await client.get("/items")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient):
    res = await client.post("/items", json={
        "name": "Test Item",
        "description": "An item for testing",
        "price": 9.99
    })
    assert res.status_code == 200
    item = res.json()
    assert item["name"] == "Test Item"
    assert item["price"] == 9.99


@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient):
    res = await client.post("/items", json={
        "name": "DeleteMeItem",
        "description": "Temporary item",
        "price": 1.99
    })
    item_id = res.json()["id"]
    res = await client.delete(f"/items/{item_id}")
    assert res.status_code == 200
    assert res.json()["ok"] is True


def test_metrics(client_sync: TestClient):
    res = client_sync.get("/metrics")
    assert res.status_code == 200
    assert b"http_requests_total" in res.content


def test_healthz(client_sync: TestClient):
    res = client_sync.get("/healthz")
    assert res.status_code == 200
    assert res.json() == {"ok": True}


@pytest.mark.asyncio
async def test_admin_access_users(client: AsyncClient):
    res = await client.post("/register", json={
        "name": "admin",
        "email": "admin@example.com",
        "password": "adminpass",
        "role": RoleEnum.ADMIN.value
    })
    res = await client.post("/login", json={
        "email": "admin@example.com",
        "password": "adminpass"
    })
    token = res.json()["access_token"]

    res = await client.get("/users", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_user_denied_access_users(client: AsyncClient):
    res = await client.post("/register", json={
        "name": "user",
        "email": "user@example.com",
        "password": "userpass",
        "role": RoleEnum.USER.value
    })
    res = await client.post("/login", json={
        "email": "user@example.com",
        "password": "userpass"
    })
    token = res.json()["access_token"]

    res = await client.get("/users", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 403


@pytest.mark.asyncio
async def test_refresh_and_logout(client: AsyncClient):
    # Register and login
    res = await client.post("/register", json={
        "name": "refresh_test",
        "email": "refresh@example.com",
        "password": "secret",
        "role": RoleEnum.USER.value
    })
    assert res.status_code == 200

    res = await client.post("/login", json={
        "email": "refresh@example.com",
        "password": "secret"
    })
    assert res.status_code == 200
    old_access_token = res.json()["access_token"]
    refresh_token_cookie = res.cookies.get("refresh_token")
    assert refresh_token_cookie

    # refresh
    res = await client.get("/refresh", cookies={"refresh_token": refresh_token_cookie})
    assert res.status_code == 200
    new_access_token = res.json()["access_token"]
    assert new_access_token != old_access_token

    # logout
    res = await client.post("/logout", cookies={"refresh_token": refresh_token_cookie})
    assert res.status_code == 200
    assert res.json() == {"ok": True}