from pydantic import BaseModel, ConfigDict, Field


class HotelCreate(BaseModel):
    title: str
    location: str


class HotelPUT(BaseModel):
    title: str
    location: str


class HotelPATCH(BaseModel):
    title: str | None = Field(default=None)
    location: str | None = Field(default=None)


class HotelSchema(HotelCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
