from fastapi import APIRouter, Body
from repositories.hotels import HotelRepository
from src.hotels.schemas import HotelCreate, HotelPATCH, HotelPUT
from src.hotels.dependencies import PaginatorDep

from database import async_session_maker


hotels = [
    {"id": 1, "title": "Sochi", "description": "Hotel in sochi"},
    {"id": 2, "title": "Moscow", "description": "Hotel in moscow"},
    {"id": 3, "title": "Berlin", "description": "Hotel in berlin"},
    {"id": 4, "title": "London", "description": "Hotel in london"},
    {"id": 5, "title": "Paris", "description": "Hotel in paris"},
    {"id": 6, "title": "Rome", "description": "Hotel in rome"},
    {"id": 7, "title": "New York", "description": "Hotel in new york"},
    {"id": 8, "title": "Tokyo", "description": "Hotel in tokyo"},
    {"id": 9, "title": "Sydney", "description": "Hotel in sydney"},
    {"id": 10, "title": "Amsterdam", "description": "Hotel in amsterdam"},
    {"id": 11, "title": "Amman", "description": "Hotel in amman"},
]

router = APIRouter(prefix="/hotels")


@router.get(
    "/", 
    summary="Получить все отели"
)
async def get_hotels(
    paginator: PaginatorDep,
    location: str | None = None,
    title: str | None = None
):
    """
    Ручка для получения всех отелей 
    с пагинацией и фильтрацией по полям `title` и `location`.

    Фильтрация не чувствительна к регистру.
    """
    offset = (paginator.page - 1) * paginator.per_page
    limit = paginator.per_page
    
    async with async_session_maker() as session:
        return await HotelRepository(session=session).get_all(
            location=location,
            title=title,
            limit=limit,
            offset=offset
        )


@router.get(
    "/{hotel_id}",
    summary="Получить отель по id",
    description="Получение отеля по его id."
)
async def get_hotel_by_id(
    hotel_id: int
):
    async with async_session_maker() as session:
        return await HotelRepository(session=session).get_one_or_none(id=hotel_id)

@router.post(
    "/",
    summary="Создать отель",
    description="Создание нового отеля.",
)
async def create_hotel(
    hotel_data: HotelCreate = Body(
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
    async with async_session_maker() as session:
        ret_hotel = await HotelRepository(session=session).add(
            hotel_data=hotel_data
        )
        await session.commit()
    
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
    hotel_id: int,
    hotel_data: HotelPUT = Body(),
):
    async with async_session_maker() as session:
        ret_hotel = await HotelRepository(session=session).edit(
            data=hotel_data,
            id=hotel_id,
        )
        await session.commit()
    
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
    hotel_id: int, 
    hotel_data: HotelPATCH = Body()
):
    async with async_session_maker() as session:
        ret_hotel = await HotelRepository(session=session).edit(
            data=hotel_data,
            exclude_unset=True,
            id=hotel_id,
        )
        await session.commit()
    
    return {
        "message": "Hotel updated",
        "data": ret_hotel
    }

@router.delete(
    "/{hotel_id}",
    summary="Удалить отель",
    description="Удаление существующего отеля по его id."
)
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        ret_hotel = await HotelRepository(session=session).delete(
            id=hotel_id
        )
        await session.commit()
    
    return {
        "message": "Hotel deleted",
        "data": ret_hotel
    }
