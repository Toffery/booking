from pydantic import BaseModel
from src.repositories.baserepo import BaseRepository
from src.facilities.models import Facility, RoomsFacilities
from src.facilities.schemas import FacilityInDB, RoomFacilityCreate, RoomFacilityInDB


class FacilityRepository(BaseRepository):
    model = Facility
    schema = FacilityInDB


class RoomFacilityRepository(BaseRepository):
    model = RoomsFacilities
    schema = RoomFacilityInDB

    async def update_or_delete(self, room_data: BaseModel, room_id: int):
        existing_facilities = await self.get_filtered(room_id=room_id)
        existing_facilities_ids = [f.facility_id for f in existing_facilities]

        facilities_ids_to_add = [f_id for f_id in room_data.facilities_ids 
                                if f_id not in existing_facilities_ids]
        facilities_ids_to_remove = [f_id for f_id in existing_facilities_ids
                                    if f_id not in room_data.facilities_ids]

        for f_id in facilities_ids_to_add:
            room_facility_create = RoomFacilityCreate(
                room_id=room_id,
                facility_id=f_id,
            )
            await self.add(room_facility_create)
        for f_id in facilities_ids_to_remove:
            await self.delete(room_id=room_id, facility_id=f_id)
    