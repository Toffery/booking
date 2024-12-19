from datetime import date

from src.hotels.schemas import HotelInDB
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
