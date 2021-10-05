from pydantic import BaseModel

from src.models import AddressType


class NewAddressSchema(BaseModel):
    class Config:
        extra = "forbid"
        use_enum_values = True

    line1: str
    line2: str = None
    city: str
    state: str
    zipcode: str
    type: AddressType
