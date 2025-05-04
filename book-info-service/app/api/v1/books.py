from fastapi import APIRouter, HTTPException
from app.services.mongo_service import MongoService
from app.services.cache_service import CacheService
from app.models.book import Book

router = APIRouter()
mongo_service = MongoService("mongodb://mongo:27017", "bookstore")
cache_service = CacheService("redis://redis:6379")

@router.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: str):
    cached = await cache_service.get(f"book:{book_id}")
    if cached:
        return Book(**eval(cached))
    record = await mongo_service.get_record("books", book_id)
    if record:
        await cache_service.set(f"book:{book_id}", str(record))
        return Book(**record)
    raise HTTPException(status_code=404, detail="Book not found")

@router.post("/books", response_model=Book)
async def create_book(book: Book):
    record = book.dict()
    created = await mongo_service.create_record("books", record)
    await cache_service.set(f"book:{book.id}", str(created))
    return Book(**created)

@router.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: str, book: Book):
    updates = book.dict(exclude={"id"})
    updated = await mongo_service.update_record("books", book_id, updates)
    if updated:
        await cache_service.set(f"book:{book_id}", str(updated))
        return Book(**updated)
    raise HTTPException(status_code=404, detail="Book not found")

@router.delete("/books/{book_id}")
async def delete_book(book_id: str):
    deleted = await mongo_service.delete_record("books", book_id)
    if deleted:
        await cache_service.delete(f"book:{book_id}")
        return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")