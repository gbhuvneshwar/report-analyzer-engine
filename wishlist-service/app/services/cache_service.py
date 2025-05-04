from redis.asyncio import Redis
from typing import Optional

class CacheService:
    def __init__(self, redis_url: str):
        self.redis = Redis.from_url(redis_url, decode_responses=True)

    async def get(self, key: str) -> Optional[str]:
        return await self.redis.get(key)

    async def set(self, key: str, value: str, expire: int = None):
        await self.redis.set(key, value, ex=expire)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def close(self):
        await self.redis.aclose()