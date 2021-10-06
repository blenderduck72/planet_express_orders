from src.models.base_model import DynamoItem


class LineItem(DynamoItem):
    """
    Represents a LineItem

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

    description : str
        LineItem's description.
    id : str
        LineItem's two digit id.
    name : str
        name of item.
    order_id : str
        id of associated order.
    quantity : int
        number of items ordered.

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

    _PK_ENTITY: str = "Order"
    _PK_FIELD: str = "order_id"
    _SK_ENTITY: str = "LineItem"
    _SK_FIELD: str = "id"

    description: str
    id: str
    name: str
    order_id: str
    quantity: int
