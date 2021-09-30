import boto3
from boto3.dynamodb.conditions import Key
from pydantic import BaseModel

from src.dynamodb.ItemFactory import ItemFactory
from src.models.customer import Customer
from src.models.order import DynamoOrder, Order


class CustomerFactory(ItemFactory):
    PK_ENTITY: str = "Customer"
    PK_FIELD: str = "email"
    SK_ENTITY: str = "User"
    SK_FIELD: str = "username"
    DDB_MODEL: BaseModel = Customer
    DOMAIN_MODEL: BaseModel = Customer


class OrderFactory(ItemFactory):
    PK_ENTITY: str = "Order"
    PK_FIELD: str = "id"
    DDB_MODEL: BaseModel = DynamoOrder
    DOMAIN_MODEL: BaseModel = Order

    @classmethod
    def create_item(cls, data: dict) -> BaseModel:
        pass
