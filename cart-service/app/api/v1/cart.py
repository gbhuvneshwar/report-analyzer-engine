from fastapi import APIRouter, HTTPException
from app.services.cache_service import CacheService
from app.services.postgres_service import PostgresService
from app.models.cart import Cart

router = APIRouter()
cache_service = CacheService("redis://redis:6379")
db_service = PostgresService("postgresql+asyncpg://user:password@postgres:5432/mydb")

@router.get("/cart/{cart_id}", response_model=Cart)
async def get_cart(cart_id: str):
    cached = await cache_service.get(f"cart:{cart_id}")
    if cached:
        return Cart(**eval(cached))
    await db_service.connect()
    try:
        record = await db_service.get_record("cart_items", cart_id)
        if record:
            await cache_service.set(f"cart:{cart_id}", str(dict(record)))
            return Cart(**record)
        return Cart(id=cart_id, user_id="", book_ids=[])
    finally:
        await db_service.close()

@router.post("/cart", response_model=Cart)
async def create_cart(cart: Cart):
    await db_service.connect()
    try:
        record = await db_service.create_record("cart_items", cart.dict())
        await cache_service.set(f"cart:{cart.id}", str(dict(record)))
        return Cart(**record)
    finally:
        await db_service.close()

@router.put("/cart/{cart_id}", response_model=Cart)
async def update_cart(cart_id: str, cart: Cart):
    await db_service.connect()
    try:
        updates = cart.dict(exclude={"id"})
        updated = await db_service.update_record("cart_items", cart_id, updates)
        if updated:
            await cache_service.set(f"cart:{cart_id}", str(dict(updated)))
            return Cart(**updated)
        raise HTTPException(status_code=404, detail="Cart not found")
    finally:
        await db_service.close()

@router.delete("/cart/{cart_id}")
async def delete_cart(cart_id: str):
    await db_service.connect()
    try:
        deleted = await db_service.delete_record("cart_items", cart_id)
        if deleted:
            await cache_service.delete(f"cart:{cart_id}")
            return {"message": "Cart deleted"}
        raise HTTPException(status_code=404, detail="Cart not found")
    finally:
        await db_service.close()