from typing import List

from pydantic import BaseModel

from src.dynamodb.ItemFactory import ItemFactory
from src.models.customer import Customer
from src.models.order import DynamoOrder, Order
from src.models.line_item import LineItem


class CustomerFactory(ItemFactory):
    PK_ENTITY: str = "Customer"
    PK_FIELD: str = "email"
    SK_ENTITY: str = "User"
    SK_FIELD: str = "username"
    DDB_MODEL: BaseModel = Customer
    DOMAIN_MODEL: BaseModel = Customer


class LineItemFactory(ItemFactory):
    PK_ENTITY: str = "Order"
    PK_FIELD: str = "order_id"
    SK_ENTITY: str = "LineItem"
    SK_FIELD: str = "id"
    DDB_MODEL: BaseModel = LineItem
    DOMAIN_MODEL: BaseModel = LineItem


class OrderFactory(ItemFactory):
    PK_ENTITY: str = "Order"
    PK_FIELD: str = "id"
    SK_ENTITY: str = None
    SK_FIELD: str = None
    DDB_MODEL: BaseModel = DynamoOrder
    DOMAIN_MODEL: BaseModel = Order
