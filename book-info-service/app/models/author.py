from pydantic import BaseModel

class Author(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True