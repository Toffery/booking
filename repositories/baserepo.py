from pydantic import BaseModel
from src.database import async_session_maker
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

class BaseRepository:
    model = None
    def __init__(self, session: Session) -> None:
        self.session = session


    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().all()
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)

        result = await self.session.execute(query)

        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().one()

    async def edit(self, data: BaseModel, **filter_by):
        stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().one()
    
    async def delete(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        # print(compile(stmt))
        result = await self.session.execute(stmt)
        return result.scalars().one()