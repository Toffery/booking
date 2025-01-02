# ruff: noqa: E402
from typing import AsyncGenerator
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest
from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
import json

from src.dependencies import get_db
from src.main import app
from src.utils.db_manager import DBManager


@pytest.fixture(
    scope="function",
)
async def db() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


async def get_db_null_pool() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(
    scope="session",
    autouse=True,
)
async def setup_database():
    # Чтобы базу не снести
    print(f"{settings.MODE=}")
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def insert_hotels_and_rooms(setup_database, ac):
    with (
        open("tests/mock_hotels.json") as hotels_file,
        open("tests/mock_rooms.json") as rooms_file,
    ):
        hotels = json.load(hotels_file)
        rooms = json.load(rooms_file)
    for hotel in hotels:
        response = await ac.post("/hotels/", json=hotel)
        assert response.status_code == 200, (
            "Failed to add hotels in db",
            response.status_code,
            response.text,
        )
    for room in rooms:
        hotel_id = room["hotel_id"]
        response = await ac.post(f"/hotels/{hotel_id}/rooms", json=room)
        assert response.status_code == 200, (
            "Failed to add rooms in db",
            response.status_code,
            response.text,
        )


@pytest.fixture(scope="session", autouse=True)
async def add_user(setup_database, ac):
    response = await ac.post(
        "/auth/signup",
        json={
            "email": "test@ya.ru",
            "password": "test",
        },
    )
    assert response.status_code == 200


@pytest.fixture(scope="session")
async def authenticated_ac(add_user, ac):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as new_ac:
        response = await ac.post(
            "/auth/login",
            json={
                "email": "test@ya.ru",
                "password": "test",
            },
        )
        assert response.status_code == 200
        assert ac.cookies["access_token"], (
            "Access token not found",
            response.status_code,
            response.text,
        )
        new_ac.cookies = {"access_token": response.json()["access_token"]}
        yield new_ac
