from pydantic import BaseModel, ConfigDict, Field


class HotelCreateOrUpdate(BaseModel):
    title: str
    location: str


class HotelPATCH(BaseModel):
    title: str | None = Field(default=None)
    location: str | None = Field(default=None)


class HotelInDB(HotelCreateOrUpdate):
    id: int

    model_config = ConfigDict(from_attributes=True)
