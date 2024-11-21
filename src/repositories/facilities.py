from src.repositories.baserepo import BaseRepository
from src.facilities.models import Facility, RoomsFacilities
from src.facilities.schemas import FacilityInDB, RoomFacilityInDB


class FacilityRepository(BaseRepository):
    model = Facility
    schema = FacilityInDB


class RoomFacilityRepository(BaseRepository):
    model = RoomsFacilities
    schema = RoomFacilityInDB
