from pydantic import BaseModel, ConfigDict


class FacilityIn(BaseModel):
    title: str


class FacilityInDB(FacilityIn):
    id: int

    model_config = ConfigDict(from_attributes=True)


class FacilityUpdate(BaseModel):
    title: str
