from fastapi import APIRouter, HTTPException
from app.services.postgres_service import PostgresService
from app.services.kafka_service import KafkaService
from app.models.order import Order

router = APIRouter()
db_service = PostgresService("postgresql+asyncpg://user:password@postgres:5432/mydb")
kafka_service = KafkaService("kafka:9092", "order-updates")

@router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    await db_service.connect()
    try:
        record = await db_service.get_record("orders", order_id)
        if record:
            await kafka_service.send_message({"order_id": order_id, "action": "get"})
            return Order(**record)
        raise HTTPException(status_code=404, detail="Order not found")
    finally:
        await db_service.close()

@router.post("/orders", response_model=Order)
async def create_order(order: Order):
    await db_service.connect()
    try:
        record = await db_service.create_record("orders", order.dict())
        await kafka_service.send_message({"order_id": order.id, "action": "create"})
        return Order(**record)
    finally:
        await db_service.close()

@router.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: str, order: Order):
    await db_service.connect()
    try:
        updates = order.dict(exclude={"id"})
        updated = await db_service.update_record("orders", order_id, updates)
        if updated:
            await kafka_service.send_message({"order_id": order_id, "action": "update"})
            return Order(**updated)
        raise HTTPException(status_code=404, detail="Order not found")
    finally:
        await db_service.close()

@router.delete("/orders/{order_id}")
async def delete_order(order_id: str):
    await db_service.connect()
    try:
        deleted = await db_service.delete_record("orders", order_id)
        if deleted:
            await kafka_service.send_message({"order_id": order_id, "action": "delete"})
            return {"message": "Order deleted"}
        raise HTTPException(status_code=404, detail="Order not found")
    finally:
        await db_service.close()