from pydantic import BaseModel, EmailStr


class NewCustomerSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    username: str
