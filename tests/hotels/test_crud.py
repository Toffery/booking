import pytest

from src.exceptions import ObjectNotFoundException
from src.hotels.schemas import HotelCreateOrUpdate, HotelPATCH


async def test_hotels_crud(db):
    hotel_to_create: HotelCreateOrUpdate = HotelCreateOrUpdate(
        title="Test Hotel",
        location="Yoshkar-Ola, Panfilova st. 1",
    )
    created_hotel = await db.hotels.add(hotel_to_create)
    assert created_hotel
    assert created_hotel.title == "Test Hotel"
    assert created_hotel.location == "Yoshkar-Ola, Panfilova st. 1"

    hotel_data_to_update = HotelCreateOrUpdate(
        title="Updated Test Hotel",
        location="Yoshkar-Ola, Panfilova st. 2",
    )
    updated_hotel = await db.hotels.edit(hotel_data_to_update, id=created_hotel.id)
    assert updated_hotel
    assert updated_hotel.title == "Updated Test Hotel"
    assert updated_hotel.location == "Yoshkar-Ola, Panfilova st. 2"

    hotel_data_to_patch = HotelPATCH(
        title="Patched Test Hotel",
    )
    patched_hotel = await db.hotels.edit(
        hotel_data_to_patch, exclude_unset=True, id=created_hotel.id
    )
    assert patched_hotel
    assert patched_hotel.title == "Patched Test Hotel"
    assert patched_hotel.location == "Yoshkar-Ola, Panfilova st. 2"

    hotel_data_to_patch = HotelPATCH(
        location="Patched location",
    )
    patched_hotel = await db.hotels.edit(
        hotel_data_to_patch, exclude_unset=True, id=created_hotel.id
    )
    assert patched_hotel
    assert patched_hotel.title == "Patched Test Hotel"
    assert patched_hotel.location == "Patched location"

    deleted_hotel = await db.hotels.delete(id=created_hotel.id)
    assert deleted_hotel

    with pytest.raises(ObjectNotFoundException):
        await db.hotels.get_one(id=created_hotel.id)
