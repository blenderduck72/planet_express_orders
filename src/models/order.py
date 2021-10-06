from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from src.models.base_model import DynamoItem
from src.models.line_item import LineItem


class OrderStatus(str, Enum):
    """
    Enum of Order Statuses.

    ...

    Attributes
    ----------
    NEW: str
        Represents a new Order.
    SUBMITTED : str
        Represents a submitted order.
    IN_PROGRESS : str
        Represents an Order that is in progress.
    FULFILLED : str
        Represents an Order that is packaged.
    SHIPPED : str
        Represents an Order that is shipped.
    OUT_FOR_DELIVERY : str
        Represents an Order that is out for delivery.
    DELIVERED : str
        Represents an Order that is complete.


    """

    NEW: str = "new"
    SUBMITTED: str = "submitted"
    IN_PROGRESS: str = "in_progress"
    FULFILLED: str = "fuliflled"
    SHIPPED: str = "shipped"
    OUT_FOR_DELIVERY: str = "out_for_delivery"
    DELIVERED: str = "delivered"


class DeliveryAddress(BaseModel):
    """
    Represents an DeliveryAddress

    ...

    Attributes
    ----------
    customer_email: str
        Email of associated customer.
    datetime_created : datetime
        Datetime of Order creation.
    delivery_address : DeliveryAddress
        Address of Order's delivery.
    id : str
        id of Order.
    item_count: int
        Count of Line Items.
    status : OrderStatus
        Enum value of an Order's Status.

    """

    line1: str
    line2: str = None
    city: str
    state: str
    zipcode: str


class DynamoOrder(DynamoItem):
    """
    Represents an Order

    ...

    Attributes
    ----------
    _PK_ENTITY : str
        Entity name of the Partition Key.
    _PK_FIELD : str
        Field with a value used to form a Partition Key.
    _SK_ENTITY : str
        Entity name of the Sort Key.
    _SK_FIELD: str
        Field with a value used to form the Sort Key.

    customer_email : str
        Email of associated customer.
    datetime_created : datetime
        Datetime of Order creation.
    delivery_address : DeliveryAddress
        Address of Order's delivery.
    id : str
        id of Order.
    item_count : int
        Count of Line Items.
    status : OrderStatus
        Enum value of an Order's Status.


    Methods
    -------
    entity() -> str:
        Returns the model's calculated entity.

    key() -> str:
        Returns the calculated key of the model.

    pk() -> str:
        Returns the calculated Partition Key.

    sk() -> str:
        Returns the calcualted Sort Key.

    Class Methods
    -------
    calculate_key(pk_value: str, sk_value: str) -> dict:
        Accepts two values and returns a calculated DynamoDB key.
    """

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
    """
    Represents a Domain Order.

    ...

    Attributes
    ----------
    _PK_ENTITY (str) : Entity name of the Partition Key.
    _PK_FIELD (str) : Field with a value used to form a Partition Key.
    _SK_ENTITY (str) : Entity name of the Sort Key.
    _SK_FIELD: (str) : Field with a value used to form the Sort Key.

    customer_email (str) : Email of associated customer.
    datetime_created (datetime) : Datetime of Order creation.
    delivery_address (DeliveryAddress) : Address of Order's delivery.
    id (str) : id of Order.
    item_count (int) : Count of Line Items.
    line_items: (List[LineItem]) : List of associated LineItems.
    status (OrderStatus) : Enum value of an Order's Status.


    Methods
    -------
    entity() -> str
        Returns the model's calculated entity.

    key() -> str
        Returns the calculated key of the model.

    pk() -> str
        Returns the calculated Partition Key.

    sk() -> str
        Returns the calcualted Sort Key.

    Class Methods
    -------
    calculate_key(pk_value: str, sk_value: str) -> dict
        Accepts two values and returns a calculated DynamoDB key.
    """

    class Config:
        use_enum_value = True
        title = "Domain Order Model"

    line_items: List[LineItem] = Field(
        [], description="Line items associated with an Order."
    )
