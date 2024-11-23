from src.repositories.baserepo import BaseRepository
from src.bookings.models import Booking
from src.bookings.schemas import BookingInDB
from src.repositories.mappers.mappers import BookingDataMapper


class BookingRepository(BaseRepository):
    model = Booking
    mapper = BookingDataMapper
