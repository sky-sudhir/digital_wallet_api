from decimal import Decimal
from hmac import new
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.models.transaction import Transaction
from src.schemas.transfer_schema import TransferError, TransferRequest


class TransferService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def transfer_money(self, transfer_detail: TransferRequest):

        sender_user = await self.session.execute(
            select(User).where(User.id == transfer_detail.sender_user_id)
        )
        sender_user = sender_user.scalar_one_or_none()
        if not sender_user:
            raise HTTPException(status_code=404, detail="Sender user does not exist")

        # Check if recipient exists
        recipient_user = await self.session.execute(
            select(User).where(User.id == transfer_detail.recipient_user_id)
        )
        recipient_user = recipient_user.scalar_one_or_none()
        if not recipient_user:
            raise HTTPException(status_code=404, detail="Recipient user does not exist")

        # Check if sender has enough balance
        if sender_user.balance < transfer_detail.amount:
            exception_response=TransferError(
              error="Insufficient balance",
              current_balance=sender_user.balance,
              required_amount=transfer_detail.amount
            )
            raise HTTPException(status_code=400, detail=exception_response)

        if isinstance(transfer_detail.amount, float):
            transfer_detail.amount = Decimal(transfer_detail.amount)
        # Perform the transfer
        sender_user.balance -= transfer_detail.amount
        recipient_user.balance += transfer_detail.amount


        new_transaction = Transaction(
            user_id=sender_user.id,
            transaction_type="TRANSFER",
            amount=transfer_detail.amount,
            description=f"Transfer to {recipient_user.id}",
            recipient_user_id=recipient_user.id,
            
        )

        self.session.add_all([sender_user, recipient_user, new_transaction])
        await self.session.commit()
        await self.session.refresh(new_transaction)

        return new_transaction

    async def get_transfer_detail(self, transfer_id: int):
        transaction = await self.session.execute(
            select(Transaction).where(Transaction.id == transfer_id)
        )
        transaction= transaction.scalar_one_or_none()

        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        return transaction