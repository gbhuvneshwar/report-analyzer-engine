from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1 import wishlist

app = FastAPI(
    title="Wishlist Service",
    version="1.0.0",
    docs_url="/docs",
)

setup_logging()

app.include_router(wishlist.router, prefix="/v1/wishlist", tags=["Wishlist"])

@app.on_event("startup")
async def startup_event():
    pass

@app.on_event("shutdown")
async def shutdown_event():
    pass