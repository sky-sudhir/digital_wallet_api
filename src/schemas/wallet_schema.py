
from pydantic import BaseModel


class WalletBalanceResponse(BaseModel):
    user_id: int
    balance: float
    last_updated: str

  




class WalletTransactionResponse(BaseModel):
    transaction_id: int
    user_id: int
    amount: float
    new_balance: float
    transaction_type: str



class WalletTransactionRequest(BaseModel):
    amount: float
    description: str | None
