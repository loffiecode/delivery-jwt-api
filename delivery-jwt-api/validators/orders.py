from pydantic import BaseModel
from typing import Optional


class OrderBase(BaseModel):
    ...

class OrderCreate(OrderBase):
    name: str
    pickUpAddress: str
    deliveryAddress: str
    weight: int
    dimensions: str
    description: Optional[str] = None

class OrderDelete(OrderBase):
    id: int