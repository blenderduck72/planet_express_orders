from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.models.line_item import LineItem


class DeliveryAddress(BaseModel):
    line1: str
    line2: str = None
    city: str
    state: str
    zipcode: str


class DynamoOrder(BaseModel):
    id: str
    customer_email: str
    datetime_created: datetime
    delivery_address: DeliveryAddress


class Order(DynamoOrder):
    id: str
    customer_email: str
    datetime_created: datetime
    line_item: List[LineItem] = []
