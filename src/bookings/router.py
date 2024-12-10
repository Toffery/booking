from fastapi import APIRouter

from src.auth.dependencies import GetUserIdDep
from src.bookings.schemas import BookingCreate, BookingIn
from src.dependencies import DBDep, PaginatorDep

from src.core.tasks.tasks import send_email_notification_on_booking_creation

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get(
    "/"
)
async def get_all_bookings(
        db: DBDep,
        paginator: PaginatorDep
):
    offset = (paginator.page - 1) * paginator.per_page
    limit = paginator.per_page
    return await db.bookings.get_all(
        limit=limit,
        offset=offset
    )


@router.get(
    "/me"
)
async def get_my_bookings(
        db: DBDep,
        user_id: GetUserIdDep
):
    return await db.bookings.get_filtered(user_id=user_id)


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
    # ret_booking = await db.bookings.add(data=_booking_data)
    try:
        ret_booking = await db.bookings.add_booking(booking_data=_booking_data)
        await db.commit()
    except:
        return {"OOOOPS"}
    user = await db.auth.get_one_or_none(id=user_id)

    send_email_notification_on_booking_creation.delay(user.email)

    return {
        "message": "Booking created",
        "data": ret_booking
    }
