from pydantic import BaseModel
from src.models.order import DeliveryAddress


class NewOrderSchema(BaseModel):
    class Config:
        extra: str = "forbid"

    customer_email: str
    delivery_address_id: str


class UpdateOrderSchema(BaseModel):
    class Config:
        extra: str = "forbid"

    status: str
    delivery_address: DeliveryAddress
