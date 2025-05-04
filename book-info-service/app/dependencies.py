from fastapi import Depends
from app.services.mongo_service import MongoService
from app.services.cache_service import CacheService

async def get_mongo_service() -> MongoService:
    return MongoService()

async def get_cache_service() -> CacheService:
    cache = CacheService()
    await cache.init()
    return cache