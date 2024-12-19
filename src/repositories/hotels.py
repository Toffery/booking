from datetime import date

from sqlalchemy import func, select, Select

from src.exceptions import DateRangeException
from src.hotels.models import Hotel
from src.hotels.schemas import HotelInDB
from src.repositories.baserepo import BaseRepository
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import get_available_rooms_ids
from src.rooms.models import Room


class HotelRepository(BaseRepository):
    model = Hotel
    mapper = HotelDataMapper

    async def get_filtered_by_date(
        self,
        date_from: date,
        date_to: date,
        location: str | None = None,
        title: str | None = None,
        limit: int = 5,
        offset: int = 0,
    ) -> list[HotelInDB]:

        if date_from >= date_to:
            raise DateRangeException

        available_rooms_ids: Select = get_available_rooms_ids(
            date_from=date_from,
            date_to=date_to,
        )
        available_hotels_ids: Select = (
            select(Room.hotel_id)
            .distinct()
            .select_from(Room)
            .filter(Room.id.in_(available_rooms_ids))
        )
        query: Select = select(Hotel).filter(Hotel.id.in_(available_hotels_ids))

        if location:
            location = location.strip().lower()
            query = query.filter(func.lower(Hotel.location).contains(location))
        if title:
            title = title.strip().lower()
            query = query.filter(func.lower(Hotel.title).contains(title))
        query = query.offset(offset).limit(limit)

        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]
