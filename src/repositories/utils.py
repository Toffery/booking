from datetime import date

from sqlalchemy import func, select

from src.bookings.models import Booking
from src.rooms.models import Room


def get_available_rooms_ids(
        date_from: date,
        date_to: date,
        hotel_id: int | None = None,
):
    """
    with FIND_OCCUPIED_ROOMS as (
            select room_id, count( *) as num_of_occupied_rooms
    from bookings
    where date_from <= '2024-10-22' and date_to >= '2024-10-15'
    group by room_id
    ),
    COUNT_FREE_ROOMS as (
        select r.id as room_id, quantity - coalesce(num_of_occupied_rooms, 0) as num_of_free_rooms
    from rooms r
    left
    join
    FIND_OCCUPIED_ROOMS
    on
    r.id = FIND_OCCUPIED_ROOMS.room_id
    )
    select *
    from COUNT_FREE_ROOMS
    where
    num_of_free_rooms > 0 and room_id in
    (select id from rooms where hotel_id = {hotel_id});
    """

    find_occupied_rooms = (
        select(Booking.room_id, func.count("*").label("num_of_occupied_rooms"))
        .select_from(Booking)
        .filter(Booking.date_from <= date_to, Booking.date_to >= date_from        )
        .group_by(Booking.room_id)
        .cte("find_occupied_rooms")
    )

    num_of_occupied_rooms = func.coalesce(find_occupied_rooms.c.num_of_occupied_rooms, 0)
    count_free_rooms = (
        select(
            Room.id.label("room_id"),
            (Room.quantity - num_of_occupied_rooms).label("num_of_free_rooms")
        )
        .join_from(
            Room,
            find_occupied_rooms,
            Room.id == find_occupied_rooms.c.room_id,
            isouter=True)
        .cte("count_free_rooms")
    )

    room_ids_of_hotel = (
        select(Room.id)
        .select_from(Room)
    )
    if hotel_id is not None:
        room_ids_of_hotel = (
            room_ids_of_hotel.filter_by(hotel_id=hotel_id)
        )
    room_ids_of_hotel = room_ids_of_hotel.subquery()

    available_rooms_ids = (
        select(count_free_rooms.c.room_id)
        .select_from(count_free_rooms)
        .filter(count_free_rooms.c.num_of_free_rooms > 0,
                count_free_rooms.c.room_id.in_(room_ids_of_hotel))
    )

    return available_rooms_ids