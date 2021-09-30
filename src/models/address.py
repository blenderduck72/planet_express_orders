from pydantic import BaseModel


class Address(BaseModel):
    id: str
    line1: str
    line2: str
    city: str
    state: str
    zipcode: str
    type: str
