from datetime import date

from src.hotels.schemas import HotelInDB, HotelCreateOrUpdate, HotelPATCH
from src.services.base import BaseService
from src.utils.utils import check_date_range_or_raise


class HotelService(BaseService):

    async def get_hotels(
        self,
        paginator,
        location: str | None,
        title: str | None,
        date_from: date,
        date_to: date,
    ) -> list[HotelInDB]:

        check_date_range_or_raise(date_from, date_to)

        offset = (paginator.page - 1) * paginator.per_page
        limit = paginator.per_page

        return await self.db.hotels.get_filtered_by_date(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=limit,
            offset=offset,
        )

    async def get_hotel_by_id(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def create_hotel(self, hotel_data: HotelCreateOrUpdate):
        hotel: HotelInDB = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def update_hotel(self, hotel_id: int, data: HotelCreateOrUpdate):
        hotel: HotelInDB = await self.db.hotels.edit(data, id=hotel_id)
        await self.db.commit()
        return hotel

    async def patch_hotel(self, hotel_id: int, data: HotelPATCH):
        hotel: HotelInDB = await self.db.hotels.edit(data, exclude_unset=True, id=hotel_id)
        await self.db.commit()
        return hotel

    async def delete_hotel(self, hotel_id: int):
        hotel: HotelInDB = await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
        return hotel