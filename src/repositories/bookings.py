from datetime import date

from fastapi import HTTPException
from sqlalchemy import select

from src.bookings.schemas import BookingCreate
from src.repositories.baserepo import BaseRepository
from src.bookings.models import Booking
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import get_available_rooms_ids
from src.rooms.models import Room


class BookingRepository(BaseRepository):
    model = Booking
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(self.model).filter(self.model.date_from == date.today())
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, booking_data: BookingCreate):
        hotel_id_query = select(Room.hotel_id).filter(Room.id == booking_data.room_id)
        result = await self.session.execute(hotel_id_query)
        hotel_id = result.scalars().one()
        available_rooms_ids = get_available_rooms_ids(
            date_from=booking_data.date_from,
            date_to=booking_data.date_to,
            hotel_id=hotel_id,
        )
        available_rooms_ids = await self.session.execute(available_rooms_ids)
        available_rooms_ids = available_rooms_ids.scalars().all()
        if booking_data.room_id in available_rooms_ids:
            return await self.add(booking_data)
        else:
            raise HTTPException(status_code=500, detail="No rooms available")
