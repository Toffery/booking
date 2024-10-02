from sqlalchemy import func, insert, select
from src.hotels.schemas import HotelInDB
from src.hotels.models import Hotel
from src.repositories.baserepo import BaseRepository


class HotelRepository(BaseRepository):
    model = Hotel
    schema = HotelInDB

    async def get_all(
        self, 
        location: str | None = None,
        title: str | None = None,
        limit: int = 5,
        offset: int = 0
    ) -> list[HotelInDB]:
        query = select(Hotel)
        if location:
            location = location.strip().lower()
            query = query.filter(func.lower(Hotel.location).contains(location))
        if title:
            title = title.strip().lower()
            query = query.filter(func.lower(Hotel.title).contains(title))
        query = (
            query
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def add(self, hotel_data: HotelInDB):
        stmt = insert(Hotel).values(**hotel_data.model_dump()).returning(Hotel)
        return await self.session.execute(stmt)
