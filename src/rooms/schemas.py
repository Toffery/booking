from pydantic import BaseModel, ConfigDict, Field


class RoomUpdate(BaseModel):
    title: str
    description: str | None
    price: int
    quantity: int


class RoomCreate(RoomUpdate):
    hotel_id: int


class RoomInDB(RoomCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPATCH(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None)
    quantity: int | None = Field(default=None)
