from typing import Literal
from pydantic import BaseModel


class TransactionCreate(BaseModel):
    user_id: int
    transaction_type: str
    amount: float
    description: str | None
    reference_transaction_id: int | None
    recipient_user_id: int | None






class TransactionRequest(BaseModel):
    user_id: int
    transaction_type: Literal["CREDIT", "DEBIT"]
    amount: float
    description: str | None