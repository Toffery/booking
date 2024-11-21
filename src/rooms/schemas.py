from pydantic import BaseModel, ConfigDict, Field


class RoomIn(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomTempWithFacilities(RoomIn):
    facilities_ids: list[int] | None = None


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

class RoomUpdateTempWithFacilities(RoomUpdate):
    facilities_ids: list[int] | None = Field(default=None)

class RoomPATCH(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None)
    quantity: int | None = Field(default=None)


class RoomPatchTempWithFacilities(RoomPATCH):
    facilities_ids: list[int] | None = Field(default=None)
