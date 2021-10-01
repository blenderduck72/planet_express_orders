from pydantic import BaseModel


class LineItem(BaseModel):
    id: str
    name: str
    description: str
    quantity: int
    order_id: str
