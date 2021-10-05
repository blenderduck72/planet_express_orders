from datetime import date

from pydantic import EmailStr
from src.models.base_model import DynamoItem


class Customer(DynamoItem):
    _PK_ENTITY: str = "Customer"
    _PK_FIELD: str = "email"
    _SK_ENTITY: str = "User"
    _SK_FIELD: str = "username"

    date_created: date
    email: EmailStr
    first_name: str
    last_name: str
    username: str
