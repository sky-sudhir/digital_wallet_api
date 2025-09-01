
from http import HTTPStatus
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.db import get_db
from src.models import user
from src.schemas.wallet_schema import WalletBalanceResponse, WalletTransactionRequest
from src.services.wallet_service import WalletService

router = APIRouter(prefix="/wallet", tags=["wallet"])

@router.get("/{user_id}/balance")
async def get_wallet_balance(user_id: int, db: AsyncSession = Depends(get_db)):
    user_balance = await WalletService(db).get_wallet_balance(user_id)
    return user_balance


@router.post("/{user_id}/add-money",status_code=HTTPStatus.CREATED)
async def add_wallet_balance(user_id: int, request_body: WalletTransactionRequest, db: AsyncSession = Depends(get_db)):
    transaction = await WalletService(db).add_wallet_balance(request_body, user_id)
    return transaction

@router.post("/{user_id}/withdraw",status_code=HTTPStatus.CREATED)
async def withdraw_wallet_balance(user_id: int, request_body: WalletTransactionRequest, db: AsyncSession = Depends(get_db)):
    transaction = await WalletService(db).withdraw_wallet_balance(request_body, user_id)
    return transaction