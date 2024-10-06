from fastapi import APIRouter, Body
from src.repositories.hotels import HotelRepository
from src.hotels.schemas import HotelCreateOrUpdate, HotelPATCH, HotelPUT
from src.hotels.dependencies import PaginatorDep

from src.database import async_session_maker


router = APIRouter(prefix="/hotels", tags=["Hotels"])


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
