from datetime import date

from pydantic import EmailStr
from src.models.base_model import DynamoItem


class Customer(DynamoItem):
    """
    Represents a Customer

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

    date_created : date
        Date customer account is created.
    email : EmailStr
        Customer's email address.
    first_name : str
        Customer's first name.
    last_name : str
        Customer's last_name.
    username : str
        Customer's username.

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

    _PK_ENTITY: str = "Customer"
    _PK_FIELD: str = "email"
    _SK_ENTITY: str = "User"
    _SK_FIELD: str = "username"

    date_created: date
    email: EmailStr
    first_name: str
    last_name: str
    username: str
