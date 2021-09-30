from datetime import datetime

from pydantic import BaseModel

from src.models.address import Address


class Order(BaseModel):
    id: str
    customer_email: str
    delivery_address: Address
    datetime_created: datetime
