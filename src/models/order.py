from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from src.models.base_model import DynamoItem
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


class DynamoOrder(DynamoItem):

    _PK_ENTITY: str = "Order"
    _PK_FIELD: str = "id"
    _SK_ENTITY: str = None
    _SK_FIELD: str = None

    class Config:
        use_enum_value = True

    customer_email: str = Field(description="Customer's email.")
    datetime_created: datetime = Field(description="Date the Order is created.")
    delivery_address: DeliveryAddress = Field("Customer's delivery address.")
    id: str = Field(description="Order id.")
    item_count: int = Field(default=0, description="Total line items in the order")
    status: OrderStatus = Field(description="Order's current status.")


class Order(DynamoOrder):
    class Config:
        use_enum_value = True
        title = "Domain Order Model"

    line_items: List[LineItem] = Field(
        [], description="Line items associated with an Order."
    )
