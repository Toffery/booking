import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))
from src.hotels.router import router as router_hotels
from src.auth.router import router as router_auth
from src.rooms.router import router as router_rooms
from src.bookings.router import router as router_bookings
from src.facilities.router import router as router_facility
from src.core.setup import redis_manager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    print("Connected to Redis")
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    await redis_manager.close()
    print("Redis connection closed")

app = FastAPI(title="Learning FastAPI", lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_facility)

@app.get("/")
async def root():
    return {
        "message": "Welcome to this amazing API!"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
