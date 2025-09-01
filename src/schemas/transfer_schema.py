from pydantic import BaseModel


class TransferRequest(BaseModel):
    sender_user_id: int
    recipient_user_id: int
    amount: float
    description: str|None


class TransferError(BaseModel):
    error: str
    current_balance: float
    required_amount: float