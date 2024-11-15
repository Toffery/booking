from datetime import date

from sqlalchemy import select

from src.rooms.schemas import RoomInDB
from src.rooms.models import Room
from src.repositories.baserepo import BaseRepository
from src.repositories.utils import get_available_rooms_ids


class RoomRepository(BaseRepository):
    model = Room
    schema = RoomInDB


    async def get_all(self, hotel_id: int):
        query = (
            select(Room)
            .filter_by(hotel_id=hotel_id)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_filtered_by_date(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        """
            Возвращаем СВОБОДНЫЕ номера для отеля {hotel_id} в период {date_from} - {date_to}
        """

        available_rooms_ids = get_available_rooms_ids(
            date_from=date_from,
            date_to=date_to,
            hotel_id=hotel_id,
        )

        return await self.get_filtered(Room.id.in_(available_rooms_ids))
