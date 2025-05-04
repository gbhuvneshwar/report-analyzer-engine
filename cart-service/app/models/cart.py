from pydantic import BaseModel

class Cart(BaseModel):
    id: str
    user_id: str
    book_ids: list[str]

    class Config:
        from_attributes = True