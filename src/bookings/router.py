from fastapi import APIRouter

from src.auth.dependencies import GetUserIdDep
from src.bookings.schemas import BookingIn, BookingCreate
from src.dependencies import DBDep

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.post(
    "/"
)
async def create_booking(
        db: DBDep,
        booking_in: BookingIn,
        user_id: GetUserIdDep
):
    room = await db.rooms.get_one_or_none(id=booking_in.room_id)
    _booking_data = BookingCreate(
        **booking_in.model_dump(),
        user_id=user_id,
        price=room.price*(booking_in.date_to - booking_in.date_from).days
    )
    ret_booking = await db.bookings.add(data=_booking_data)
    await db.commit()

    return {
        "message": "Booking created",
        "data": ret_booking
    }
