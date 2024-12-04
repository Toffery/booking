import pytest
from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.database import Base, engine_null_pool
import httpx

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
