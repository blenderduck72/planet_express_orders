from src.models.base_model import DynamoItem


class LineItem(DynamoItem):
    _PK_ENTITY: str = "Order"
    _PK_FIELD: str = "order_id"
    _SK_ENTITY: str = "LineItem"
    _SK_FIELD: str = "id"

    description: str
    id: str
    name: str
    order_id: str
    quantity: int
