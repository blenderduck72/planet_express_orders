from datetime import datetime
from enum import Enum

from pydantic import EmailStr

from src.models.base_model import DynamoItem


class AddressType(str, Enum):
    DELIVERY: str = "delivery"
    BILLING: str = "billing"


class Address(DynamoItem):
    class Config:
        use_enum_value = True

    _PK_ENTITY: str = "Customer"
    _PK_FIELD: str = "email"
    _SK_ENTITY: str = "Address"
    _SK_FIELD: str = "id"

    city: str
    line1: str
    line2: str = None
    id: str
    state: str
    type: AddressType
    zipcode: str


class DynamoAddress(Address):
    email: EmailStr
    datetime_created: datetime
