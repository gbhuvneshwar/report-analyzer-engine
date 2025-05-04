from fastapi import APIRouter, Depends, HTTPException
from app.models.author import Author, AuthorCreate, AuthorUpdate
from app.services.mongo_service import MongoService
from app.services.cache_service import CacheService
from app.dependencies import get_mongo_service, get_cache_service

router = APIRouter()

@router.post("/", response_model=Author)
async def create_author(
    author: AuthorCreate,
    mongo_service: MongoService = Depends(get_mongo_service),
    cache_service: CacheService = Depends(get_cache_service)
):
    db_author = await mongo_service.create_author(author)
    await cache_service.set_author(db_author.id, db_author)
    return db_author

@router.get("/{author_id}", response_model=Author)
async def get_author(
    author_id: str,
    mongo_service: MongoService = Depends(get_mongo_service),
    cache_service: CacheService = Depends(get_cache_service)
):
    cached_author = await cache_service.get_author(author_id)
    if cached_author:
        return cached_author
    db_author = await mongo_service.get_author(author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    await cache_service.set_author(author_id, db_author)
    return db_author

@router.put("/{author_id}", response_model=Author)
async def update_author(
    author_id: str,
    author: AuthorUpdate,
    mongo_service: MongoService = Depends(get_mongo_service),
    cache_service: CacheService = Depends(get_cache_service)
):
    db_author = await mongo_service.update_author(author_id, author)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    await cache_service.set_author(author_id, db_author)
    return db_author

@router.delete("/{author_id}")
async def delete_author(
    author_id: str,
    mongo_service: MongoService = Depends(get_mongo_service),
    cache_service: CacheService = Depends(get_cache_service)
):
    success = await mongo_service.delete_author(author_id)
    if not success:
        raise HTTPException(status_code=404, detail="Author not found")
    await cache_service.delete_author(author_id)
    return {"message": "Author deleted"}