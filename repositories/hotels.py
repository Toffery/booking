from src.hotels.models import Hotel
from repositories.baserepo import BaseRepository


class HotelRepository(BaseRepository):
    model = Hotel
