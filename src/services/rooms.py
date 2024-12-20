from datetime import date

from src.exceptions import ObjectNotFoundException, HotelNotFoundException, RoomNotFoundException
from src.facilities.schemas import RoomFacilityCreate
from src.rooms.schemas import RoomCreate, RoomIn, RoomInDB, RoomPatchIn, RoomPatch, RoomUpdateIn, RoomUpdate
from src.services.base import BaseService
from src.services.hotels import HotelService
from src.utils.utils import check_date_range_or_raise


class RoomService(BaseService):
    async def get_rooms(self, hotel_id: int, date_from: date, date_to: date):
        check_date_range_or_raise(date_from, date_to)

        try:
            _ = await HotelService(self.db).get_hotel_by_id(hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        return await self.db.rooms.get_filtered_by_date(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room_by_room_id(self, hotel_id: int, room_id: int):
        try:
            _ = await HotelService(self.db).get_hotel_by_id(hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        try:
            return await self.db.rooms.get_one(id=room_id, hotel_id=hotel_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException

    async def create_room(self, hotel_id: int, room_data: RoomIn):
        try:
            _ = await HotelService(self.db).get_hotel_by_id(hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        # TODO: add checking if facilities exist
        _room_data = RoomCreate(hotel_id=hotel_id, **room_data.model_dump())
        created_room: RoomInDB = await self.db.rooms.add(_room_data)
        if room_data.facilities_ids:
            room_facilities = [
                RoomFacilityCreate(room_id=created_room.id, facility_id=facility_id)
                for facility_id in room_data.facilities_ids
            ]
            await self.db.rooms_facilities.add_bulk(room_facilities)
        await self.db.commit()
        return created_room

    async def patch_room(self, hotel_id: int, room_id: int, room_data: RoomPatchIn):
        _: RoomInDB = await self.get_room_by_room_id(hotel_id, room_id)
        data = RoomPatch(**room_data.model_dump(exclude_unset=True))
        patched_room = None
        if any(val is not None for val in data.model_dump().values()):
            patched_room = await self.db.rooms.edit(
                data=data, id=room_id, hotel_id=hotel_id, exclude_unset=True
            )

        await self.db.rooms_facilities.update(room_data, room_id)
        await self.db.commit()

        return patched_room

    async def update_room(self, hotel_id: int, room_id: int, room_data: RoomUpdateIn):
        _: RoomInDB = await self.get_room_by_room_id(hotel_id, room_id)
        data = RoomUpdate(**room_data.model_dump(exclude={"facilities_ids"}))
        updated_room = await self.db.rooms.edit(
            data=data,
            exclude_unset=True,
            id=room_id,
            hotel_id=hotel_id
        )
        await self.db.rooms_facilities.update(room_data, room_id)
        await self.db.commit()
        return updated_room

    async def delete_room(self, hotel_id: int, room_id: int):
        _: RoomInDB = await self.get_room_by_room_id(hotel_id, room_id)
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()
        return {"message": "Room deleted"}