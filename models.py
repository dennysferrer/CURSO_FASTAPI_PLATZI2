from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlmodel import SQLModel, Field



class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: Optional[str] = Field(default=None)
    email: EmailStr
    age: int

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    #id: str = str(uuid.uuid4())
    id: int | None = Field(default=None, primary_key=True)


class Transaction(BaseModel):
    id: int
    amount: int
    description: str


class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def ammount_total(self):
        return sum(transaction.amount for transaction in self.transactions)