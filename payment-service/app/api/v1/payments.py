from fastapi import APIRouter, HTTPException
from app.services.postgres_service import PostgresService
from app.services.kafka_service import KafkaService
from app.models.payment import Payment

router = APIRouter()
db_service = PostgresService("postgresql+asyncpg://user:password@postgres:5432/mydb")
kafka_service = KafkaService("kafka:9092", "payment-updates")

@router.get("/payments/{payment_id}", response_model=Payment)
async def get_payment(payment_id: str):
    await db_service.connect()
    try:
        record = await db_service.get_record("payments", payment_id)
        if record:
            await kafka_service.send_message({"payment_id": payment_id, "action": "get"})
            return Payment(**record)
        raise HTTPException(status_code=404, detail="Payment not found")
    finally:
        await db_service.close()

@router.post("/payments", response_model=Payment)
async def create_payment(payment: Payment):
    await db_service.connect()
    try:
        record = await db_service.create_record("payments", payment.dict())
        await kafka_service.send_message({"payment_id": payment.id, "action": "create"})
        return Payment(**record)
    finally:
        await db_service.close()

@router.put("/payments/{payment_id}", response_model=Payment)
async def update_payment(payment_id: str, payment: Payment):
    await db_service.connect()
    try:
        updates = payment.dict(exclude={"id"})
        updated = await db_service.update_record("payments", payment_id, updates)
        if updated:
            await kafka_service.send_message({"payment_id": payment_id, "action": "update"})
            return Payment(**updated)
        raise HTTPException(status_code=404, detail="Payment not found")
    finally:
        await db_service.close()

@router.delete("/payments/{payment_id}")
async def delete_payment(payment_id: str):
    await db_service.connect()
    try:
        deleted = await db_service.delete_record("payments", payment_id)
        if deleted:
            await kafka_service.send_message({"payment_id": payment_id, "action": "delete"})
            return {"message": "Payment deleted"}
        raise HTTPException(status_code=404, detail="Payment not found")
    finally:
        await db_service.close()