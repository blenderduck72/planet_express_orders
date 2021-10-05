from pydantic import BaseModel


class NewLineItemSchema(BaseModel):
    class Config:
        extra = "forbid"

    name: str
    description: str
    quantity: int
