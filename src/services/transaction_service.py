from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Transaction, User
from src.schemas.transaction_schema import TransactionRequest


class TransactionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_transaction(self, transaction_data: TransactionRequest):

        exist_user= await self.session.execute(select(User).where(User.id == transaction_data.user_id))
        exist_user= exist_user.scalar_one_or_none()

        if not exist_user:
            raise HTTPException(status_code=404, detail="User not found")

        if transaction_data.amount <= 0:
            raise HTTPException(status_code=400, detail="insufficient amount")

        if isinstance(transaction_data.amount, float):
            transaction_data.amount = Decimal(transaction_data.amount)

        if transaction_data.transaction_type == "DEBIT":
            exist_user.balance -= transaction_data.amount
        else:
            exist_user.balance += transaction_data.amount

        new_transaction = Transaction(
            user_id=transaction_data.user_id,
            transaction_type=transaction_data.transaction_type,
            amount=transaction_data.amount,
            description=transaction_data.description
        )

        
        self.session.add_all([exist_user, new_transaction])
        await self.session.commit()
        await self.session.refresh(new_transaction)
        return new_transaction
    
    async def get_transaction_detail(self, transaction_id: int):
        transaction = await self.session.execute(select(Transaction).where(Transaction.id == transaction_id))

        transaction= transaction.scalar_one_or_none()

        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        return transaction

    async def get_user_transactions(self, user_id: int, page: int, limit: int):
        exist_user = await self.session.execute(select(User).where(User.id == user_id))
        exist_user = exist_user.scalar_one_or_none()

        if not exist_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        query = select(Transaction).where(Transaction.user_id == user_id)
        result = await self.session.execute(query.offset((page - 1) * limit).limit(limit))
        return result.scalars().all()