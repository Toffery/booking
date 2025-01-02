from src.exceptions import ObjectNotFoundException, FacilityNotFoundException
from src.facilities.schemas import FacilityIn
from src.services.base import BaseService


class FacilityService(BaseService):
    async def get_facilities(self):
        return await self.db.facilities.get_all()

    async def get_facility_by_id(self, facility_id: int):
        try:
            return await self.db.facilities.get_one(id=facility_id)
        except ObjectNotFoundException:
            raise FacilityNotFoundException

    async def create_facility(self, facility_data: FacilityIn):
        created_facility = await self.db.facilities.add(facility_data)
        await self.db.commit()
        return created_facility

    async def update_facility(self, facility_id: int, facility_data: FacilityIn):
        try:
            updated_facility = await self.db.facilities.edit(facility_data, id=facility_id)
            await self.db.commit()
            return updated_facility
        except ObjectNotFoundException:
            raise FacilityNotFoundException

    async def delete_facility(self, facility_id: int):
        try:
            deleted_facility = await self.db.facilities.delete(id=facility_id)
            await self.db.commit()
            return deleted_facility
        except ObjectNotFoundException:
            raise FacilityNotFoundException
