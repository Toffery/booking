from pydantic import BaseModel
from src.database import async_session_maker
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session: Session) -> None:
        self.session = session


    async def get_filtered(self, *filters, **filter_by):
        query = (
            select(self.model)
            .filter(*filters)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)

        return [self.schema.model_validate(model) for model in result.scalars().all()]


    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()
    

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)

        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        
        if model is None:
            return None
        return self.schema.model_validate(model)


    async def add(self, data: BaseModel):
        stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model)


    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalars().one()
    

    async def delete(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().one()
