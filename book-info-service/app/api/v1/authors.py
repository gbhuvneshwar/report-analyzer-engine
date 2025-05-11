from fastapi import APIRouter, Depends, HTTPException
from app.models.author import Author
from app.services.mongo_service import MongoService
from app.services.cache_service import CacheService
from app.dependencies import get_mongo_service, get_cache_service

router = APIRouter()



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
