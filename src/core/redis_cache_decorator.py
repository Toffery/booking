import asyncio
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent.parent))

from src.facilities.schemas import FacilityInDB

from src.core.setup import redis_manager


def redis_cache(exp: int):
    def wrapper(func):
        async def inner(*args, **kwargs):
            kwargs_sep = ':'
            kwargs_list = [func.__name__]
            for key, value in kwargs.items():
                kwargs_list.append(f"{key}_{value}")
            key_for_redis = kwargs_sep.join(kwargs_list)
            cached_result = await redis_manager.get(key=key_for_redis)
            if cached_result:
                print("Getting res from cache")
                return json.loads(cached_result)
            else:
                results_from_db = await func(**kwargs)
                dumped = json.dumps(results_from_db.model_dump())
                await redis_manager.set(key=key_for_redis, value=dumped,exp=exp)
                return results_from_db
        return inner
    return wrapper

@redis_cache(exp=10)
async def to_decorate(page: int = 1, per_page: int = 10):
    print("Going to database")
    return FacilityInDB(id=1, title="Title")

async def main():
    await redis_manager.connect()
    print(await to_decorate(page=10, per_page=30))
    print(await to_decorate(page=10, per_page=30))
    print(await to_decorate(page=10, per_page=30))
    # await to_decorate(page=10, per_page=30)
    # await asyncio.sleep(15)
    # await to_decorate(page=5, per_page=10)
    # await to_decorate(page=10, per_page=30)
    # await to_decorate(page=10, per_page=30)
    await redis_manager.close()

if __name__ == "__main__":
    asyncio.run(main())

