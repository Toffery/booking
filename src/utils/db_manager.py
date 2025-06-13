from src.repositories.auth import AuthRepository
from src.repositories.bookings import BookingRepository
from src.repositories.facilities import FacilityRepository, RoomFacilityRepository
from src.repositories.hotels import HotelRepository
from src.repositories.rooms import RoomRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.hotels = HotelRepository(session=self.session)
        self.rooms = RoomRepository(session=self.session)
        self.auth = AuthRepository(session=self.session)
        self.bookings = BookingRepository(session=self.session)
        self.facilities = FacilityRepository(session=self.session)
        self.rooms_facilities = RoomFacilityRepository(session=self.session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
