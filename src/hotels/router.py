from datetime import date
from fastapi import Query
from fastapi_cache.decorator import cache

from fastapi import APIRouter, Body

from src.exceptions import DateRangeException
from src.exceptions import ObjectNotFoundException
from src.hotels.schemas import HotelCreateOrUpdate, HotelPATCH
from src.dependencies import PaginatorDep, DBDep
from src.httpexceptions import HotelNotFoundHTTPException, DateRangeHTTPException
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/", summary="Получить все отели")
@cache(expire=60)
async def get_hotels(
    paginator: PaginatorDep,
    db: DBDep,
    location: str | None = None,
    title: str | None = None,
    date_from: date = Query(examples=["2024-10-18"]),
    date_to: date = Query(examples=["2024-10-25"]),
):
    """
    Ручка для получения всех отелей
    с пагинацией и фильтрацией по полям `title` и `location`.

    Фильтрация не чувствительна к регистру.
    """
    try:
        return await HotelService(db).get_hotels(
            paginator=paginator,
            location=location,
            title=title,
            date_from=date_from,
            date_to=date_to,
        )
    except DateRangeException:
        raise DateRangeHTTPException


@router.get(
    "/{hotel_id}", summary="Получить отель по id", description="Получение отеля по его id."
)
async def get_hotel_by_id(
    hotel_id: int,
    db: DBDep,
):
    try:
        return await HotelService(db).get_hotel_by_id(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


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
                },
            },
            "2": {
                "summary": "Лучший отель",
                "value": {
                    "title": "The best Hotel",
                    "location": "Yoshkar-Ola, Panfilova st. 1",
                },
            },
        }
    ),
):
    created_hotel = await HotelService(db).create_hotel(hotel_data)
    return {"message": "Hotel added", "data": created_hotel}


@router.put(
    "/{hotel_id}",
    summary="Обновить отель",
    description="Обновление существующего отеля.",
)
async def update_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelCreateOrUpdate = Body(),
):
    try:
        updated_hotel = await HotelService(db).update_hotel(hotel_id, hotel_data)
        return {"message": "Hotel updated", "data": updated_hotel}
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.patch(
    "/{hotel_id}",
    summary="Обновить отдельную информацию об отеле",
    description="Обновление существующего отеля. \
        Возможно как обновить какие-либо поля по отдельности, так и полностью, \
        но для полного обновления лучше воспользоваться ручкой с методом PUT 'Обновить отель'.",
)
async def patch_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPATCH = Body()):
    try:
        patched_hotel = await HotelService(db).patch_hotel(hotel_id, hotel_data)
        return {"message": "Hotel updated", "data": patched_hotel}
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.delete(
    "/{hotel_id}", summary="Удалить отель", description="Удаление существующего отеля по его id."
)
async def delete_hotel(db: DBDep, hotel_id: int):
    try:
        deleted_hotel = await HotelService(db).delete_hotel(hotel_id)
        return {"message": "Hotel deleted", "data": deleted_hotel}
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException