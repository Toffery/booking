from typing import TypeVar, Protocol

from pydantic import BaseModel
from sqlalchemy import Row, RowMapping

from src.database import Base


ModelType = TypeVar("ModelType", bound=Base)
DomainEntityType = TypeVar("DomainEntityType", bound=BaseModel)


class DataMapper(Protocol[ModelType, DomainEntityType]):
    db_model: type[ModelType]
    schema: type[DomainEntityType]

    @classmethod
    def map_to_domain_entity(cls, data: ModelType | dict | Row | RowMapping) -> DomainEntityType:
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data: DomainEntityType) -> ModelType:
        return cls.db_model(**data.model_dump())
