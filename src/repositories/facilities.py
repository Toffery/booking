from src.repositories.baserepo import BaseRepository
from src.facilities.models import Facility
from src.facilities.schemas import FacilityInDB


class FacilityRepository(BaseRepository):
    model = Facility
    schema = FacilityInDB
