from sqlalchemy import delete

from src.repositories.baserepo import BaseRepository
from src.facilities.models import Facility, RoomFacility
from src.facilities.schemas import RoomFacilityCreate
from src.repositories.mappers.mappers import FacilityDataMapper, RoomFacilityDataMapper
from src.rooms.schemas import RoomIn, RoomPatchIn, RoomUpdateIn


class FacilityRepository(BaseRepository[Facility, FacilityDataMapper]):
    model = Facility
    mapper = FacilityDataMapper


class RoomFacilityRepository(BaseRepository[RoomFacility, RoomFacilityDataMapper]):
    model = RoomFacility
    mapper = RoomFacilityDataMapper

    async def update(self, room_data: RoomIn | RoomPatchIn | RoomUpdateIn, room_id: int):
        existing_facilities = await self.get_filtered(room_id=room_id)
        existing_facilities_ids = [f.facility_id for f in existing_facilities]

        if not room_data.facilities_ids:
            return

        facilities_ids_to_add = [
            f_id for f_id in room_data.facilities_ids if f_id not in existing_facilities_ids
        ]
        facilities_ids_to_remove = [
            f_id for f_id in existing_facilities_ids if f_id not in room_data.facilities_ids
        ]

        if facilities_ids_to_add:
            rooms_facilities_to_add = [
                RoomFacilityCreate(room_id=room_id, facility_id=f_id)
                for f_id in facilities_ids_to_add
            ]
            await self.add_bulk(rooms_facilities_to_add)
        if facilities_ids_to_remove:
            stmt = delete(self.model).filter(
                self.model.room_id == room_id, self.model.facility_id.in_(facilities_ids_to_remove)
            )
            await self.session.execute(stmt)
