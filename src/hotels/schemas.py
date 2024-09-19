from pydantic import BaseModel


class HotelCreate(BaseModel):
    title: str
    location: str

class HotelUpdate(HotelCreate):
    id: int

class HotelPUT(BaseModel):
    title: str | None = None
    location: str | None = None
