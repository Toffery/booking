from fastapi import APIRouter
from src.hotels.schemas import Hotel, HotelPUT
from src.hotels.dependencies import PaginatorDep


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
    description="Ручка для получения всех отелей с пагинацией",
    summary="Получить все отели"
)
async def get_hotels(
    paginator: PaginatorDep
):
    start = (paginator.page - 1) * paginator.per_page
    end = start + paginator.per_page
    return {
        "page": paginator.page,
        "per_page": paginator.per_page,
        "hotels": hotels[start:end]
    }

@router.post(
    "/",
    summary="Создать отель",
    description="Создание нового отеля.",
)
async def create_hotel(hotel: Hotel):
    new_hotel = hotel.model_dump()
    hotels.append(new_hotel)
    print(hotels)
    return {"message": "Hotel added"}

@router.put(
    "/",
    summary="Обновить отель",
    description="Обновление существующего отеля.",
)
async def update_hotel(
    hotel_data: Hotel,
):
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_data.id][0]
    hotel["title"] = hotel_data.title
    hotel["description"] = hotel_data.description
    print(hotels)
    return hotel

@router.patch(
    "/{hotel_id}",
    summary="Обновить отдельную информацию об отеле",
    description="Обновление существующего отеля. \
        Возможно как обновить какие-либо поля по отдельности, так и полностью, \
        но для полного обновления лучше воспользоваться ручкой с методом PUT 'Обновить отель'."
)
async def patch_hotel(
    hotel_id: int, 
    hotel_data: HotelPUT
):
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.description:
        hotel["description"] = hotel_data.description
    print(hotels)
    return hotel

@router.delete(
    "/{hotel_id}",
    summary="Удалить отель",
    description="Удаление существующего отеля по его id."
)
async def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"message": "Hotel deleted"}
