from pydantic import BaseModel


class Hotel(BaseModel):
    id: int
    title: str
    description: str

class HotelPUT(BaseModel):
    title: str | None = None
    description: str | None = None
