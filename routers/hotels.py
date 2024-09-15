from fastapi import APIRouter
from schemas.hotels import Hotel, HotelPUT


hotels = [
    {"id": 1, "title": "Sochi", "description": "Hotel in sochi"},
    {"id": 2, "title": "Moscow", "description": "Hotel in moscow"},
]

router = APIRouter(prefix="/hotels")

@router.get("/")
async def root():
    return {"message": "Hello from FastAPI"}

@router.get("/hotels")
async def get_hotels():
    return hotels

@router.post("/hotels")
async def create_hotel(hotel: Hotel):
    new_hotel = hotel.model_dump()
    hotels.append(new_hotel)
    print(hotels)
    return {"message": "Hotel added"}

@router.put("/hotels")
async def update_hotel(
    hotel_data: Hotel,
):
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_data.id][0]
    hotel["title"] = hotel_data.title
    hotel["description"] = hotel_data.description
    print(hotels)
    return hotel

@router.patch("/hotels/{hotel_id}")
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

@router.delete("/hotels/{hotel_id}")
async def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"message": "Hotel deleted"}
