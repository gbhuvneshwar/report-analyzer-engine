from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1 import books, authors

app = FastAPI(
    title="Book Info Service",
    version="1.0.0",
    docs_url="/docs",
)

setup_logging()

app.include_router(books.router, prefix="/v1/books", tags=["Books"])
app.include_router(authors.router, prefix="/v1/authors", tags=["Authors"])

@app.on_event("startup")
async def startup_event():
    pass

@app.on_event("shutdown")
async def shutdown_event():
    pass