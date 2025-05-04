from fastapi import Depends
from app.services.postgres_service import PostgresService
from app.services.kafka_service import KafkaService

async def get_postgres_service() -> PostgresService:
    service = PostgresService()
    await service.init()
    return service

async def get_kafka_service() -> KafkaService:
    service = KafkaService()
    await service.init()
    return service