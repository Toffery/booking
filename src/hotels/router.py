from datetime import date
from fastapi import Query

from fastapi import APIRouter, Body
from src.hotels.schemas import HotelCreateOrUpdate, HotelPATCH, HotelPUT
from src.dependencies import PaginatorDep, DBDep


router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get(
    "/", 
    summary="Получить все отели"
)
async def get_hotels(
        paginator: PaginatorDep,
        db: DBDep,
        location: str | None = None,
        title: str | None = None,
        date_from: date = Query(example="2024-10-18"),
        date_to: date = Query(example="2024-10-25"),
):
    """
    Ручка для получения всех отелей 
    с пагинацией и фильтрацией по полям `title` и `location`.

    Фильтрация не чувствительна к регистру.
    """
    # offset = (paginator.page - 1) * paginator.per_page
    # limit = paginator.per_page
    #
    # return await db.hotels.get_all(
    #     location=location,
    #     title=title,
    #     limit=limit,
    #     offset=offset
    # )

    return await db.hotels.get_filtered_by_date(
        date_from=date_from,
        date_to=date_to,
    )


@router.get(
    "/{hotel_id}",
    summary="Получить отель по id",
    description="Получение отеля по его id."
)
async def get_hotel_by_id(
        hotel_id: int,
        db: DBDep,
):
    return await db.hotels.get_one_or_none(id=hotel_id)

@router.post(
    "/",
    summary="Создать отель",
    description="Создание нового отеля.",
)
async def create_hotel(
        db: DBDep,
        hotel_data: HotelCreateOrUpdate = Body(
            openapi_examples={
                "1": {
                    "summary": "Абстрактный отель",
                    "value": {
                        "title": "New Hotel",
                        "location": "Abstract Hotel location",
                    }
                },
                "2": {
                    "summary": "Лучший отель",
                    "value": {
                        "title": "The best Hotel",
                        "location": "Yoshkar-Ola, Panfilova st. 1",
                    }
                },
            }
        )
):
    ret_hotel = await db.hotels.add(hotel_data=hotel_data)
    await db.commit()
    
    return {
        "message": "Hotel added",
        "data": ret_hotel.scalars().all()
    }

@router.put(
    "/{hotel_id}",
    summary="Обновить отель",
    description="Обновление существующего отеля.",
)
async def update_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelPUT = Body(),
):
    ret_hotel = await db.hotels.edit(
        data=hotel_data,
        id=hotel_id,
    )
    await db.commit()
    
    return {
        "message": "Hotel updated",
        "data": ret_hotel
    }

@router.patch(
    "/{hotel_id}",
    summary="Обновить отдельную информацию об отеле",
    description="Обновление существующего отеля. \
        Возможно как обновить какие-либо поля по отдельности, так и полностью, \
        но для полного обновления лучше воспользоваться ручкой с методом PUT 'Обновить отель'."
)
async def patch_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPATCH = Body()
):
    ret_hotel = await db.hotels.edit(
        data=hotel_data,
        exclude_unset=True,
        id=hotel_id,
    )
    await db.commit()

    return {
        "message": "Hotel updated",
        "data": ret_hotel
    }

@router.delete(
    "/{hotel_id}",
    summary="Удалить отель",
    description="Удаление существующего отеля по его id."
)
async def delete_hotel(
        db: DBDep,
        hotel_id: int
):
    ret_hotel = await db.hotels.delete(id=hotel_id)
    await db.commit()
    
    return {
        "message": "Hotel deleted",
        "data": ret_hotel
    }
