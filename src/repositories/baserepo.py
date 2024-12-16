from typing import Sequence, Generic, TypeVar, Any

from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base
from sqlalchemy import delete, insert, select, update

from src.exceptions import ObjectNotFoundException
from src.repositories.mappers.base import DataMapper


ModelType = TypeVar("ModelType", bound=Base)
DataMapperType = TypeVar("DataMapperType", bound=DataMapper)
DomainEntityType = TypeVar("DomainEntityType", bound=BaseModel)


class BaseRepository(Generic[ModelType, DataMapperType]):
    model: type[ModelType]
    mapper: type[DataMapperType]
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_filtered(self, *filters, **filter_by):
        query = select(self.model).filter(*filters).filter_by(**filter_by)
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

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException

        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel, exclude_unset: bool = False):
        stmt = (
            insert(self.model)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: Sequence[BaseModel]) -> None:
        stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(stmt)

    async def edit(
            self,
            data: BaseModel,
            exclude_unset: bool = False,
            **filter_by
    ) -> Any | BaseModel:
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalars().one()

    async def delete(self, **filter_by) -> BaseModel | Any:
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().one()

    async def delete_all_rows(self) -> None:
        await self.session.execute(delete(self.model))
