from fastapi import Depends
from app.services.postgres_service import PostgresService
from app.services.cache_service import CacheService

async def get_postgres_service() -> PostgresService:
    service = PostgresService()
    await service.init()
    return service

async def get_cache_service() -> CacheService:
    service = CacheService()
    await service.init()
    return service