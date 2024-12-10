from pydantic import BaseModel
from src.database import Base
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model: Base = None
    mapper: DataMapper = None

    def __init__(self, session: Session) -> None:
        self.session = session

    async def get_filtered(self, *filters, **filter_by):
        query = (
            select(self.model)
            .filter(*filters)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)

        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: list[BaseModel]):
        stmt = (
            insert(self.model)
            .values([item.model_dump() for item in data])
        )
        await self.session.execute(stmt)

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

    async def delete_all_rows(self):
        await self.session.execute(delete(self.model))
