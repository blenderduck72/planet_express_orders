from typing import List

from pydantic import BaseModel

from src.dynamodb.ItemFactory import ItemFactory
from src.models import (
    Address,
    Customer,
    DynamoAddress,
    DynamoOrder,
    Order,
    LineItem,
)


class AddressFactory(ItemFactory):
    PK_ENTITY: str = "Customer"
    PK_FIELD: str = "email"
    SK_ENTITY: str = "Address"
    SK_FIELD: str = "id"
    DDB_MODEL: BaseModel = DynamoAddress
    DOMAIN_MODEL: Address = Address


class CustomerFactory(ItemFactory):
    PK_ENTITY: str = "Customer"
    PK_FIELD: str = "email"
    SK_ENTITY: str = "User"
    SK_FIELD: str = "username"
    DDB_MODEL: Customer = Customer
    DOMAIN_MODEL: Customer = Customer


class LineItemFactory(ItemFactory):
    PK_ENTITY: str = "Order"
    PK_FIELD: str = "order_id"
    SK_ENTITY: str = "LineItem"
    SK_FIELD: str = "id"
    DDB_MODEL: LineItem = LineItem
    DOMAIN_MODEL: LineItem = LineItem


class OrderFactory(ItemFactory):
    PK_ENTITY: str = "Order"
    PK_FIELD: str = "id"
    SK_ENTITY: str = None
    SK_FIELD: str = None
    DDB_MODEL: DynamoOrder = DynamoOrder
    DOMAIN_MODEL: Order = Order
