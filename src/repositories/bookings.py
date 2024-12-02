from datetime import date

from sqlalchemy import select

from src.repositories.baserepo import BaseRepository
from src.bookings.models import Booking
from src.repositories.mappers.mappers import BookingDataMapper


class BookingRepository(BaseRepository):
    model = Booking
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(self.model)
            .filter(self.model.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]
