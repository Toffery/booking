import pytest

from src.config import settings
from src.database import Base, engine_null_pool
# from src.users.models import User
# from src.hotels.models import Hotel
# from src.rooms.models import Room
# from src.bookings.models import Booking
# from src.facilities.models import Facility, RoomFacility


@pytest.fixture(
    scope="session",
    autouse=True
)
async def async_main():

    # Чтобы базу не снести
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
