from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.exceptions import DateRangeException
from src.repositories.mappers.mappers import RoomDataMapper
from src.rooms.schemas import RoomWithFacilities
from src.rooms.models import Room
from src.repositories.baserepo import BaseRepository
from src.repositories.utils import get_available_rooms_ids


class RoomRepository(BaseRepository[Room, RoomDataMapper]):
    model = Room
    mapper = RoomDataMapper

    async def get_all_by_hotel(self, hotel_id: int):
        query = select(Room).filter_by(hotel_id=hotel_id)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_one_or_none_with_facilities(self, **filter_by):
        query = (
            select(self.model).options(selectinload(self.model.facilities)).filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if result is None:
            return None
        return RoomWithFacilities.model_validate(model)

    async def get_filtered_by_date(self, hotel_id: int, date_from: date, date_to: date):
        """
        Возвращаем СВОБОДНЫЕ номера для отеля {hotel_id} в период {date_from} - {date_to}
        """
        if date_from >= date_to:
            raise DateRangeException

        available_rooms_ids = get_available_rooms_ids(
            date_from=date_from,
            date_to=date_to,
            hotel_id=hotel_id,
        )

        stmt = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(self.model.id.in_(available_rooms_ids))
        )
        result = await self.session.execute(stmt)
        return [RoomWithFacilities.model_validate(model) for model in result.scalars().all()]
