from src.database import async_session_maker_null_pool, async_session_maker
from src.hotels.schemas import HotelCreateOrUpdate
from src.utils.db_manager import DBManager



async def test_create_hotel():
    hotel_data = HotelCreateOrUpdate(
        title="Test hotel3",
        location="Test location3"
    )
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        ret_hotel = await db.hotels.add(hotel_data=hotel_data)
        await db.commit()

        assert ret_hotel

