from sqlalchemy import func, insert, select
from src.hotels.models import Hotel
from repositories.baserepo import BaseRepository


class HotelRepository(BaseRepository):
    model = Hotel

    async def get_all(self, 
        location: str | None = None,
        title: str | None = None,
        limit: int = 5,
        offset: int = 0
    ):
        query = select(self.model)
        async with self.session.begin():
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
        return result.scalars().all()

    async def add(self, hotel_data: dict):
        stmt = insert(self.model).values(**hotel_data).returning(self.model)
        return await self.session.execute(stmt)
