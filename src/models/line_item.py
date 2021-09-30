from pydantic import BaseModel


class LineItem(BaseModel):
    id: int
    name: str
    description: str
    quantity: int
