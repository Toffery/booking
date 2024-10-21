import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI
import uvicorn

from src.hotels.router import router as router_hotels
from src.auth.router import router as router_auth
from src.rooms.router import router as router_rooms
from src.bookings.router import router as router_bookings


app = FastAPI(title="Learning FastAPI")

app.include_router(router_auth)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)

@app.get("/")
async def root():
    return {
        "message": "Welcome to this amazing API!"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
