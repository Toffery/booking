from datetime import date

from fastapi import APIRouter, Body

from src.auth.dependencies import GetAdminIdDep
from src.dependencies import DBDep
from src.exceptions import DateRangeException, HotelNotFoundException, RoomNotFoundException
from src.httpexceptions import (
    DateRangeHTTPException,
    RoomNotFoundHTTPException,
    HotelNotFoundHTTPException,
)
from src.rooms.schemas import RoomIn, RoomUpdateIn, RoomPatchIn
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get(
    "/{hotel_id}/rooms",
    summary="Получить все свободные номера для конкретного отеля для переданных дат",
)
async def get_rooms(hotel_id: int, db: DBDep, date_from: date, date_to: date):
    try:
        return await RoomService(db).get_rooms(hotel_id, date_from, date_to)
    except DateRangeException:
        raise DateRangeHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить конкретный номер конкретного отеля")
async def get_single_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await RoomService(db).get_room_by_room_id(hotel_id, room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("/{hotel_id}/rooms", summary="Создать номер")
async def create_room(
    hotel_id: int,
    db: DBDep,
    admin_id: GetAdminIdDep,
    room_data: RoomIn = Body(
        openapi_examples={
            "1": {
                "summary": "Абстрактная комната",
                "value": {
                    "title": "Abstract room",
                    "description": "Abstract room description",
                    "price": 1000,
                    "quantity": 2,
                    "facilities_ids": [5, 6],
                },
            },
            "2": {
                "summary": "Лучшая комната",
                "value": {
                    "title": "Best Room",
                    "description": "Best Room description",
                    "price": 2000,
                    "quantity": 3,
                    "facilities_ids": [7, 8, 9],
                },
            },
        }
    ),
):
    try:
        created_room = await RoomService(db).create_room(hotel_id, room_data)
        return {"message": "Room created!", "data": created_room}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Обновить отдельную информацию о номере конкретного отеля",
)
async def patch_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
    admin_id: GetAdminIdDep,
    room_data: RoomPatchIn = Body(),
):
    """
    Обновление существующей комнаты.

    Возможно как обновить какие-либо поля по отдельности,
    так и полностью, но для полного обновления лучше
    воспользоваться ручкой с методом PUT 'Обновить комнату'.
    """
    try:
        patched_room = await RoomService(db).patch_room(hotel_id, room_id, room_data)
        return {"message": "Room updated", "data": patched_room}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.put(
    "/{hotel_id}/rooms/{room_id}", summary="Полностью обновить данные о номере конкретного отеля"
)
async def update_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
    admin_id: GetAdminIdDep,
    room_data: RoomUpdateIn = Body(),
):
    """
    Обновление существующей комнаты.

    Возможно как обновить какие-либо поля по отдельности,
    так и полностью, но для полного обновления лучше
    воспользоваться ручкой с методом PUT 'Обновить комнату'.
    """
    try:
        updated_room = await RoomService(db).update_room(hotel_id, room_id, room_data)
        return {"message": "Room updated", "data": updated_room}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удалить номер",
)
async def delete_room(hotel_id: int, room_id: int, db: DBDep, admin_id: GetAdminIdDep):
    try:
        await RoomService(db).delete_room(hotel_id, room_id)
        return {"message": "Room deleted"}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
