from fastapi import Depends, Query
from pydantic import BaseModel

from typing import Annotated


class PaginatorParams(BaseModel):
    page: Annotated[int | None, Query(default=1, ge=1)]
    per_page: Annotated[int | None, Query(default=5, ge=1, le=30)]


PaginatorDep = Annotated[PaginatorParams, Depends()]