import pytest
from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.database import Base, engine_null_pool
import httpx
import json

from src.main import app


@pytest.fixture(
    scope="session",
    autouse=True,
)
async def setup_database():
    # Чтобы базу не снести
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(
    scope="session",
    autouse=True
)
async def insert_hotels_and_rooms(setup_database):
    with open("tests/mock_hotels.json") as f1, open("tests/mock_rooms.json") as f2:
        hotels = json.load(f1)
        rooms = json.load(f2)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        for hotel in hotels:
            response = await ac.post("/hotels/", json=hotel)
            assert response.status_code == 200, ("Failed to add hotels in db", response.status_code, response.text)
        for room in rooms:
            hotel_id = room["hotel_id"]
            print(room)
            response = await ac.post(
                f"/hotels/{hotel_id}/rooms",
                json=room
            )
            assert response.status_code == 200, ("Failed to add rooms in db", response.status_code, response.text)


@pytest.fixture(
    scope="session",
    autouse=True
)
async def add_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/auth/signup",
            json={
                "email": "test@ya.ru",
                "password": "test",
            }
        )
        assert response.status_code == 200
