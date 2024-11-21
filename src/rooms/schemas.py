from pydantic import BaseModel, ConfigDict, Field

from src.facilities.schemas import FacilityInDB


class RoomBase(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomIn(RoomBase):
    facilities_ids: list[int] | None = None


class RoomCreate(RoomBase):
    hotel_id: int


class RoomInDB(RoomCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomWithFacilities(RoomInDB):
    facilities: list["FacilityInDB"]


class RoomUpdate(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomUpdateIn(RoomUpdate):
    facilities_ids: list[int] | None = Field(default=None)


class RoomPatch(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None)
    quantity: int | None = Field(default=None)


class RoomPatchIn(RoomPatch):
    facilities_ids: list[int] | None = Field(default=None)
