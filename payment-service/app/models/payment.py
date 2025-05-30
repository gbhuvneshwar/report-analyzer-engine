from pydantic import BaseModel

class Payment(BaseModel):
    id: str
    order_id: str
    amount: float
    status: str

    class Config:
        from_attributes = True