from datetime import date

from src.bookings.schemas import BookingCreate
from src.rooms.schemas import RoomInDB
from src.users.schemas import UserInDB


async def test_booking_crud(db):
    users: list[UserInDB] = await db.auth.get_all()
    user_id = users[0].id
    rooms: list[RoomInDB] = await db.rooms.get_all()
    room_id = rooms[0].id
    booking_data = BookingCreate(
        room_id=room_id,
        user_id=user_id,
        date_from=date(2024, 10, 18),
        date_to=date(2024, 10, 25),
        price=1000,
    )
    ret_booking = await db.bookings.add(booking_data)
    assert ret_booking

    read_booking = await db.bookings.get_one_or_none(id=ret_booking.id)
    assert read_booking, "Booking wasn't added to db"
    assert read_booking.price == 1000, "Price isn't equal to provided"
    assert read_booking.date_from == date(2024, 10, 18), "date_from isn't equal to provided"
    assert read_booking.date_to == date(2024, 10, 25), "date_to isn't equal to provided"

    update_booking = BookingCreate(
        room_id=room_id,
        user_id=user_id,
        date_from=date(2024, 12, 18),
        date_to=date(2024, 12, 25),
        price=3000,
    )
    ret_booking = await db.bookings.edit(update_booking, id=read_booking.id)
    assert ret_booking.date_from == date(2024, 12, 18), "date_from isn't equal to provided"
    assert ret_booking.date_to == date(2024, 12, 25), "date_to isn't equal to provided"
    assert ret_booking.price == 3000, "Price isn't equal to provided"
    assert ret_booking.id == read_booking.id

    await db.bookings.delete(id=ret_booking.id)
    await db.commit()

    ret_booking_after_delete = await db.bookings.get_one_or_none(id=ret_booking.id)
    assert ret_booking_after_delete is None, "Booking wasn't deleted"
