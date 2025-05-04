from pydantic import BaseModel

class Wishlist(BaseModel):
    id: str
    user_id: str
    book_ids: list[str]

    class Config:
        from_attributes = True