from fastapi import Body, FastAPI, Query
import uvicorn


app = FastAPI(title="Learning FastAPI")

hotels = [
    {"id": 1, "title": "Sochi", "description": "Hotel in sochi"},
    {"id": 2, "title": "Moscow", "description": "Hotel in moscow"},
]


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}

@app.get("/hotels")
async def get_hotels():
    return hotels

@app.post("/hotels")
async def add_hotel(hotel: dict):
    hotels.append(hotel)
    print(hotels)
    return {"message": "Hotel added"}

@app.put("/hotels")
async def update_hotel(
    hotel_data: dict,
):
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_data["id"]][0]
    hotel["title"] = hotel_data["title"]
    hotel["description"] = hotel_data["description"]
    print(hotels)
    return hotel

@app.patch("/hotels/{hotel_id}")
async def patch_hotel(
    hotel_id: int, 
    title: str | None = None,
    description: str | None = None
):
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if title:
        hotel["title"] = title
    if description:
        hotel["description"] = description
    print(hotels)
    return hotel

@app.delete("/hotels/{hotel_id}")
async def delete_hotel(hotel_id: int):
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"message": "Hotel deleted"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
