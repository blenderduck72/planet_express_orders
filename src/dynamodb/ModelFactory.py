from pydantic import BaseModel

from src.dynamodb.ItemFactory import ItemFactory
from src.models.customer import Customer
from src.models.order import Order


class CustomerFactory(ItemFactory):
    PK_ENTITY: str = "Customer"
    PK_FIELD: str = "email"
    SK_ENTITY: str = "User"
    SK_FIELD: str = "username"
    BASE_MODEL: BaseModel = Customer


class OrderFactory(ItemFactory):
    PK_ENTITY: str = "Order"
    PK_FIELD: str = "id"
    BASE_MODEL: BaseModel = Order
