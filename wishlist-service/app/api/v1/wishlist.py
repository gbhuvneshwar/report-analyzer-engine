from fastapi import APIRouter, HTTPException
from app.services.cache_service import CacheService
from app.services.postgres_service import PostgresService
from app.models.wishlist import Wishlist

router = APIRouter()
cache_service = CacheService("redis://redis:6379")
db_service = PostgresService("postgresql+asyncpg://user:password@postgres:5432/mydb")

@router.get("/wishlist/{wishlist_id}", response_model=Wishlist)
async def get_wishlist(wishlist_id: str):
    cached = await cache_service.get(f"wishlist:{wishlist_id}")
    if cached:
        return Wishlist(**eval(cached))
    await db_service.connect()
    try:
        record = await db_service.get_record("wishlists", wishlist_id)
        if record:
            await cache_service.set(f"wishlist:{wishlist_id}", str(dict(record)))
            return Wishlist(**record)
        return Wishlist(id=wishlist_id, user_id="", book_ids=[])
    finally:
        await db_service.close()

@router.post("/wishlist", response_model=Wishlist)
async def create_wishlist(wishlist: Wishlist):
    await db_service.connect()
    try:
        record = await db_service.create_record("wishlists", wishlist.dict())
        await cache_service.set(f"wishlist:{wishlist.id}", str(dict(record)))
        return Wishlist(**record)
    finally:
        await db_service.close()

@router.put("/wishlist/{wishlist_id}", response_model=Wishlist)
async def update_wishlist(wishlist_id: str, wishlist: Wishlist):
    await db_service.connect()
    try:
        updates = wishlist.dict(exclude={"id"})
        updated = await db_service.update_record("wishlists", wishlist_id, updates)
        if updated:
            await cache_service.set(f"wishlist:{wishlist_id}", str(dict(updated)))
            return Wishlist(**updated)
        raise HTTPException(status_code=404, detail="Wishlist not found")
    finally:
        await db_service.close()

@router.delete("/wishlist/{wishlist_id}")
async def delete_wishlist(wishlist_id: str):
    await db_service.connect()
    try:
        deleted = await db_service.delete_record("wishlists", wishlist_id)
        if deleted:
            await cache_service.delete(f"wishlist:{wishlist_id}")
            return {"message": "Wishlist deleted"}
        raise HTTPException(status_code=404, detail="Wishlist not found")
    finally:
        await db_service.close()