from pydantic import BaseModel, ConfigDict


class FacilityIn(BaseModel):
    title: str


class FacilityInDB(FacilityIn):
    id: int

    model_config = ConfigDict(from_attributes=True)


class FacilityUpdate(BaseModel):
    title: str


class RoomFacilityCreate(BaseModel):
    room_id: int
    facility_id: int


class RoomFacilityIn(BaseModel):
    room_id: int
    facility_id: int


class RoomFacilityInDB(RoomFacilityIn):
    id: int

    model_config = ConfigDict(from_attributes=True)
