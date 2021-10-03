from pydantic import BaseModel, EmailStr


class NewCustomerSchema(BaseModel):
    class Config:
        extra = "forbid"

    email: EmailStr
    first_name: str
    last_name: str
    username: str
