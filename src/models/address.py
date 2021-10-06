from datetime import datetime
from enum import Enum

from pydantic import EmailStr

from src.models.base_model import DynamoItem


class AddressType(str, Enum):
    """
    Enum that represent Address Types.

    ...

    Attributes
    ----------
    DELIVERY (str) : Designates an address as deliverable.
    BILLING (str) : Designates an address as billable.
    """

    DELIVERY: str = "delivery"
    BILLING: str = "billing"


class Address(DynamoItem):
    """
    Represents an Address

    ...

    Attributes
    ----------
    _PK_ENTITY : str
        Entity name of the Partition Key.
    _PK_FIELD : str
        Field with a value used to form a Partition Key.
    _SK_ENTITY : str
        Entity name of the Sort Key.
    _SK_FIELD: str
        Field with a value used to form the Sort Key.

    city : str
    line1 : str
    line2 : str
    id : str
    state : str
    type : AddressType
    zipcode : str

    Methods
    -------
    entity() -> str:
        Returns the model's calculated entity.

    key() -> str:
        Returns the calculated key of the model.

    pk() -> str:
        Returns the calculated Partition Key.

    sk() -> str:
        Returns the calcualted Sort Key.

    Class Methods
    -------
    calculate_key(pk_value: str, sk_value: str) -> dict:
        Accepts two values and returns a calculated DynamoDB key.
    """

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
    """
    Represents an Address

    ...

    Attributes
    ----------
    _PK_ENTITY : str
        Entity name of the Partition Key.
    _PK_FIELD : str
        Field with a value used to form a Partition Key.
    _SK_ENTITY : str
        Entity name of the Sort Key.
    _SK_FIELD: str
        Field with a value used to form the Sort Key.


    city : str
    datetime_created : datetime
    email : str
    line1 : str
    line2 : str
    id : str
    state : str
    type : AddressType
    zipcode : str

    Methods
    -------
    entity() -> str:
        Returns the model's calculated entity.

    key() -> str:
        Returns the calculated key of the model.

    pk() -> str:
        Returns the calculated Partition Key.

    sk() -> str:
        Returns the calcualted Sort Key.

    Class Methods
    -------
    calculate_key(pk_value: str, sk_value: str) -> dict:
        Accepts two values and returns a calculated DynamoDB key.
    """

    email: EmailStr
    datetime_created: datetime
