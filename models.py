from pydantic import BaseModel, EmailStr
from typing import Optional


class Customer(BaseModel):
    name: str
    description: Optional[str] = None
    email: EmailStr
    age: int


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