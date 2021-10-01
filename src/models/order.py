from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field, validator

from src.models.line_item import LineItem


class OrderStatus(str, Enum):
    NEW: str = "new"
    SUBMITTED: str = "submitted"
    IN_PROGRESS: str = "in_progress"
    FULFILLED: str = "fuliflled"
    SHIPPED: str = "shipped"
    OUT_FOR_DELIVERY: str = "out_for_delivery"
    DELIVERED: str = "delivered"


class DeliveryAddress(BaseModel):
    line1: str
    line2: str = None
    city: str
    state: str
    zipcode: str


class DynamoOrder(BaseModel):
    class Config:
        use_enum_value = True

    id: str
    customer_email: str = Field(description="Customer's email.")
    datetime_created: datetime = Field(description="Date the Order is created.")
    delivery_address: DeliveryAddress = Field("Customer's delivery address.")
    status: OrderStatus = Field(description="Order's current status.")
    item_count: int = Field(description="Total line items in the order")


class Order(DynamoOrder):
    line_items: List[LineItem] = Field(
        [], description="Line items associated with an Order."
    )
