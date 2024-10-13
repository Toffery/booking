from src.repositories.baserepo import BaseRepository
from src.bookings.models import Booking
from src.bookings.schemas import BookingInDB


class BookingRepository(BaseRepository):
    model = Booking
    schema = BookingInDB
