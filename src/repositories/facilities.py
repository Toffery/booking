from src.repositories.baserepo import BaseRepository


class FacilitiesRepository(BaseRepository):
    model = Facility
    schema = FacilitiyInDb