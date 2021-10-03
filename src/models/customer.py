from datetime import date

from pydantic import BaseModel, EmailStr


class Customer(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    username: str
    date_created: date
