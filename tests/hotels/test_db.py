from src.hotels.schemas import HotelCreateOrUpdate


async def test_create_hotel(db):
    hotel_data = HotelCreateOrUpdate(
        title="Test hotel",
        location="Test location"
    )
    ret_hotel = await db.hotels.add(hotel_data=hotel_data)
    await db.commit()

    assert ret_hotel
