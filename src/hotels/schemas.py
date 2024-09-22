from pydantic import BaseModel, Field


class HotelCreate(BaseModel):
    title: str
    location: str


class HotelPUT(BaseModel):
    title: str
    location: str


class HotelPATCH(BaseModel):
    title: str | None = Field(default=None)
    location: str | None = Field(default=None)
