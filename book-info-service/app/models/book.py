from pydantic import BaseModel

class Book(BaseModel):
    id: str
    title: str
    author_id: str

    class Config:
        from_attributes = True