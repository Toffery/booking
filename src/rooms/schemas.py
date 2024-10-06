from pydantic import BaseModel, ConfigDict, Field


class RoomIn(BaseModel):
    title: str
    description: str | None
    price: int
    quantity: int


class RoomCreate(RoomIn):
    hotel_id: int


class RoomInDB(RoomCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomUpdate(BaseModel):
    title: str
    description: str | None
    price: int
    quantity: int


class RoomPATCH(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None)
    quantity: int | None = Field(default=None)
