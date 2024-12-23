from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport

from src.main import app
from tests.conftest import get_db_null_pool


@pytest.fixture(
    scope="module",
)
async def delete_users():
    async for _db in get_db_null_pool():
        await _db.auth.delete_all_rows()
        await _db.commit()


@pytest.fixture(scope="function")
async def temp_ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as temp_ac:
        yield temp_ac


@pytest.mark.parametrize(
    "email, username, password_signup, password_login, status_code_signup, status_code_login",
    [
        ("test@ya.ru", "test", "test", "test", 200, 200),
        ("test@ya.ru", "test", "testtest", "test", 409, 200),
        ("test1@ya.ru", "test1", "test", "test1", 200, 401),
        (None, "testtest", "test", "test", 200, 200),
        (None, "testtest", "test1", "test1", 409, 401),
    ],
)
async def test_auth_workflow(
    email,
    username,
    password_signup,
    password_login,
    status_code_signup,
    status_code_login,
    delete_users,
    temp_ac,
):
    if username and email:
        response_signup = await temp_ac.post(
            "/auth/signup",
            json={"email": email, "username": username, "password": password_signup},
        )
    elif email:
        response_signup = await temp_ac.post(
            "/auth/signup", json={"email": email, "password": password_signup}
        )
    elif username:
        response_signup = await temp_ac.post(
            "/auth/signup", json={"username": username, "password": password_signup}
        )
    else:
        assert True
        return
    assert response_signup.status_code == status_code_signup, (
        "Failed to signup",
        response_signup.status_code,
        response_signup.text,
    )

    response_login = await temp_ac.post(
        "/auth/login", json={"username": username, "password": password_login}
    )

    if response_login.status_code == 401:
        return

    assert temp_ac.cookies.get("access_token")
    assert response_login.status_code == status_code_login, (
        "Failed to login",
        response_login.status_code,
        response_login.text,
    )

    temp_ac.cookies.set("access_token", temp_ac.cookies.get("access_token"))

    response_me = await temp_ac.get(
        "/auth/me",
    )

    assert "password" not in response_me.json()["data"]
    assert "hashed_password" not in response_me.json()["data"]

    assert response_me.status_code == 200, (
        "Failed to get me",
        response_me.status_code,
        response_me.text,
    )
    assert response_me.json()["data"]["username"] == username
    assert response_me.json()["data"]["email"] == email

    response_logout = await temp_ac.post(
        "/auth/logout",
    )
    assert response_logout.cookies.get("access_token") is None
    assert response_logout.status_code == 200, response_logout.text

    temp_ac.cookies.clear()

    response_me = await temp_ac.get(
        "/auth/me",
    )

    assert response_me.status_code == 401, (
        "Authorized after logout",
        response_me.status_code,
        response_me.text,
    )
