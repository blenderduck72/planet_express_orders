from datetime import date

from pydantic import EmailStr

from pydantic import BaseModel


class Customer(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    username: str
    date_created: date
