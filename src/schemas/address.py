from pydantic import BaseModel


class NewAddressSchema(BaseModel):
    class Config:
        extra = "forbid"

    line1: str
    line2: str
    city: str
    state: str
    zipcode: str
    type: str
