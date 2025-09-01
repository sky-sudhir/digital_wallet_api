from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Transaction, User
from src.schemas.wallet_schema import WalletTransactionRequest


class WalletService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_wallet_balance(self,user_id:int):
        exist_user= await self.session.execute(select(User).where(User.id == user_id))
        exist_user= exist_user.scalar_one_or_none()

        if not exist_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "user_id": user_id,
            "balance": exist_user.balance,
            "last_updated": exist_user.updated_at
            }

    async def add_wallet_balance(self,request_body:WalletTransactionRequest,user_id:int):

        exist_user= await self.session.execute(select(User).where(User.id == user_id))
        exist_user= exist_user.scalar_one_or_none()

        if not exist_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if isinstance(request_body.amount, float):
            request_body.amount = Decimal(request_body.amount)

        exist_user.balance += request_body.amount

        new_transaction=Transaction(
            user_id=user_id,
            amount=request_body.amount,
            transaction_type="CREDIT"
        )

        self.session.add_all([exist_user,new_transaction])
        await self.session.commit()
        await self.session.refresh(new_transaction)

        return {
            "transaction_id": new_transaction.id,
            "user_id": user_id,
            "amount": request_body.amount,
            "transaction_type": "CREDIT"
        }
    
    async def withdraw_wallet_balance(self,request_body:WalletTransactionRequest,user_id:int):
        exist_user= await self.session.execute(select(User).where(User.id == user_id))
        exist_user= exist_user.scalar_one_or_none()

        if not exist_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if request_body.amount <= 0:
            raise HTTPException(status_code=400, detail="insufficient balance")

        if isinstance(request_body.amount, float):
            request_body.amount = Decimal(request_body.amount)

        if exist_user.balance < request_body.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        exist_user.balance -= request_body.amount

        new_transaction=Transaction(
            user_id=user_id,
            amount=request_body.amount,
            transaction_type="DEBIT"
        )

        self.session.add_all([exist_user,new_transaction])
        await self.session.commit()
        await self.session.refresh(new_transaction)

        return {
            "transaction_id": new_transaction.id,
            "user_id": user_id,
            "amount": request_body.amount,
            "transaction_type": "DEBIT"
        }
