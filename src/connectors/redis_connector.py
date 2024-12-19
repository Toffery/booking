import redis.asyncio as redis

import logging


class RedisConnector:
    _redis: redis.Redis

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def connect(self):
        logging.info(f"Connecting to Redis at {self.host}:{self.port}")
        self._redis = await redis.Redis(host=self.host, port=self.port)
        logging.info(f"Successfully connected to Redis at {self.host}:{self.port}")

    async def set(self, key: str, value: str, exp: int | None = None):
        if exp:
            await self._redis.set(key, value, exp)
        else:
            await self._redis.set(key, value)

    async def get(self, key: str):
        return await self._redis.get(key)

    async def delete(self, key):
        await self._redis.delete(key)

    async def close(self):
        if self._redis:
            await self._redis.aclose()
