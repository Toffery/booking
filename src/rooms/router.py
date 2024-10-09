from fastapi import APIRouter, Body

from src.dependencies import DBDep
from src.rooms.schemas import RoomCreate, RoomPATCH, RoomUpdate, RoomIn


router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get(
    "/{hotel_id}/rooms",
    summary="Получить все комнаты отеля",
)
async def get_rooms(
        hotel_id: int,
        db: DBDep
):
    return await db.rooms.get_all(hotel_id=hotel_id)


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получить конкретный номер конкретного отеля"
)
async def get_single_room(
        hotel_id: int,
        room_id: int,
        db: DBDep
):
    return await db.rooms.get_one_or_none(
        hotel_id=hotel_id,
        id=room_id
    )


@router.post(
    "/{hotel_id}/rooms",
    summary="Создать комнату"
)
async def create_room(
        hotel_id: int,
        db: DBDep,
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

    ret_room = await db.rooms.add(data=_room_data)
    await db.commit()

    return {
        "message": "Room created!",
        "data": ret_room
    }


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Обновить отдельную информацию о комнате конкретного отеля",
)
async def patch_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomPATCH = Body()
):
    """
    Обновление существующей комнаты.

    Возможно как обновить какие-либо поля по отдельности, 
    так и полностью, но для полного обновления лучше 
    воспользоваться ручкой с методом PUT 'Обновить комнату'.
    """

    ret_room = await db.rooms.edit(
        data=room_data,
        id=room_id,
        hotel_id=hotel_id,
        exclude_unset=True
    )
    await db.commit()

    return {
        "message": "Room updated",
        "data": ret_room
    }


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Полностью обновить данные о комнате конкретного отеля"
)
async def update_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomUpdate = Body()
):
    """
    Обновление существующей комнаты.

    Возможно как обновить какие-либо поля по отдельности, 
    так и полностью, но для полного обновления лучше 
    воспользоваться ручкой с методом PUT 'Обновить комнату'.
    """
    ret_room = await db.rooms.edit(
        data=room_data,
        id=room_id,
        hotel_id=hotel_id,
        exclude_unset=False
    )
    await db.commit()

    return {
        "message": "Room updated",
        "data": ret_room
    }


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удалить комнату",
)
async def delete_room(
        hotel_id: int,
        room_id: int,
        db: DBDep
):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {
        "message": "Room deleted"
    }
