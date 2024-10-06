from fastapi import APIRouter, Body
from src.database import async_session_maker

from src.repositories.rooms import RoomRepository
from src.rooms.schemas import RoomCreate, RoomPATCH, RoomUpdate, RoomIn

router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get(
    "/{hotel_id}/rooms",
    summary="Получить все комнаты отеля",
)
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomRepository(session=session).get_all(hotel_id)


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получить конкретный номер конкретного отеля"
)
async def get_single_room(
    hotel_id: int,
    room_id: int
):
    async with async_session_maker() as session:
        return await RoomRepository(session=session).get_one_or_none(
            hotel_id=hotel_id,
            id=room_id
        )


@router.post(
    "/{hotel_id}/rooms",
    summary="Создать комнату"
)
async def create_room(
    hotel_id: int,
    room_data: RoomIn = Body(
        openapi_examples={
            "1": {
                "summary": "Абстрактная комната",
                "value": {
                    "title": "Abstract room",
                    "description": "Abstract room description",
                    "price": 1000,
                    "quantity": 2
                }
            },
            "2": {
                "summary": "Лучшая комната",
                "value": {
                    "title": "Best Room",
                    "description": "Best Room description",
                    "price": 2000,
                    "quantity": 3
                }
            }
        }
    )
):
    _room_data = RoomCreate(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomRepository(session=session).add(data=_room_data)
        await session.commit()
    return room


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Обновить отдельную информацию о комнате конкретного отеля",
)
async def patch_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPATCH = Body()
):
    """
    Обновление существующей комнаты.

    Возможно как обновить какие-либо поля по отдельности, 
    так и полностью, но для полного обновления лучше 
    воспользоваться ручкой с методом PUT 'Обновить комнату'.
    """
    async with async_session_maker() as session:
        room = await RoomRepository(session=session).edit(
            data=room_data,
            exclude_unset=True,
            id=room_id,
            hotel_id=hotel_id
        )
        await session.commit()
    return {
        "message": "Room updated",
        "data": room
    }


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Полностью обновить данные о комнате конкретного отеля"
)
async def update_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomUpdate = Body()
):
    """
    Обновление существующей комнаты.

    Возможно как обновить какие-либо поля по отдельности, 
    так и полностью, но для полного обновления лучше 
    воспользоваться ручкой с методом PUT 'Обновить комнату'.
    """
    async with async_session_maker() as session:
        room = await RoomRepository(session=session).edit(
            data=room_data,
            exclude_unset=False,
            id=room_id,
            hotel_id=hotel_id
        )
        await session.commit()
    return {
        "message": "Room updated",
        "data": room
    }


# Need to think about path
@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удалить комнату",
)
async def delete_room(
    hotel_id: int,
    room_id: int
):
    async with async_session_maker() as session:
        await RoomRepository(session=session).delete(
            id=room_id,
            hotel_id=hotel_id
        )
        await session.commit()
    return {
        "message": "Room deleted"
    }
