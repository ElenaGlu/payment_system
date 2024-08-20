from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    email: str
    hashed_password: str
    admin: bool


class AccountBaseSchema(BaseModel):
    balance: int


class PayBaseSchema(BaseModel):
    amount: int
    signature: str
