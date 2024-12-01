import functools
import json

from pydantic import BaseModel

from src.core.setup import redis_manager


def redis_cache(exp: int):
    def wrapper(func):
        @functools.wraps(func)
        async def inner(*args, **kwargs):
            kwargs_sep = ':'
            kwargs_list = [func.__name__]
            for key, value in kwargs.items():
                if key != "db":
                    kwargs_list.append(f"{key}_{value}")
            key_for_redis = kwargs_sep.join(kwargs_list)
            cached_result = await redis_manager.get(key=key_for_redis)
            if cached_result:
                print("Getting res from cache")
                return json.loads(cached_result)
            else:
                print(*args)
                results_from_db = await func(*args, **kwargs)
                if isinstance(results_from_db, list):
                    dumped = json.dumps([res.model_dump() for res in results_from_db])
                elif isinstance(results_from_db, BaseModel):
                    dumped = json.dumps(results_from_db.model_dump())
                await redis_manager.set(
                    key=key_for_redis, 
                    value=dumped,
                    exp=exp
                )
                return results_from_db
        return inner
    return wrapper
