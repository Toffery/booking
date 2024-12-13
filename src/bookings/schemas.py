from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingIn(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingCreate(BookingIn):
    price: int
    user_id: int


class BookingInDB(BookingCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)