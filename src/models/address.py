from datetime import datetime
from pydantic import BaseModel, EmailStr



class Address(BaseModel):
    id: str
    line1: str
    line2: str
    city: str
    state: str
    zipcode: str
    type: str


class DynamoAddress(Address):
    email: EmailStr
    datetime_created: datetime
