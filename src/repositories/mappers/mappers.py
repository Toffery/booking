from src.bookings.models import Booking
from src.bookings.schemas import BookingInDB
from src.facilities.models import Facility, RoomFacility
from src.facilities.schemas import FacilityInDB, RoomFacilityInDB
from src.repositories.mappers.base import DataMapper
from src.hotels.models import Hotel
from src.hotels.schemas import HotelInDB
from src.rooms.models import Room
from src.rooms.schemas import RoomInDB
from src.users.models import User
from src.users.schemas import UserInDB


class HotelDataMapper(DataMapper):
    db_model = Hotel
    schema = HotelInDB


class UserDataMapper(DataMapper):
    db_model = User
    schema = UserInDB


class BookingDataMapper(DataMapper):
    db_model = Booking
    schema = BookingInDB


class FacilityDataMapper(DataMapper):
    db_model = Facility
    schema = FacilityInDB


class RoomDataMapper(DataMapper):
    db_model = Room
    schema = RoomInDB


class RoomFacilityDataMapper(DataMapper):
    db_model = RoomFacility
    schema = RoomFacilityInDB
