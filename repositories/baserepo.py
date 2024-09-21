from src.database import async_session_maker
from sqlalchemy import insert, select, update

class BaseRepository:
    model = None
    def __init__(self, session) -> None:
        self.session = session


    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().all()
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)

        result = await self.session.execute(query)

        return result.scalars().one_or_none()

    async def add(self, *args, **kwargs):
        async with self.session.bigen():
            stmt = insert(self.model).values(**kwargs)
            await self.session.execute(stmt)
        return "Updated"
