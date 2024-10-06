from sqlalchemy import func, insert, select
from src.rooms.schemas import RoomInDB, RoomCreate
from src.rooms.models import Room
from src.repositories.baserepo import BaseRepository


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
