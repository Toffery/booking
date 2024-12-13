from typing import Annotated

from fastapi import Depends, Query

from pydantic import BaseModel

from src.database import async_session_maker
from src.utils.db_manager import DBManager


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


class PaginatorParams(BaseModel):
    page: Annotated[int | None, Query(default=1, ge=1)]
    per_page: Annotated[int | None, Query(default=30, ge=1, le=100)]

    def __repr__(self):
        return f"PaginatorParams(page={self.page}, per_page={self.per_page})"


PaginatorDep = Annotated[PaginatorParams, Depends()]
