from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr


class AddressType(str, Enum):
    DELIVERY: str = "delivery"
    BILLING: str = "billing"


class Address(BaseModel):
    class Config:
        use_enum_value = True

    id: str
    line1: str
    line2: str = None
    city: str
    state: str
    zipcode: str
    type: AddressType


class DynamoAddress(Address):
    email: EmailStr
    datetime_created: datetime
