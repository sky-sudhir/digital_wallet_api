

from http import HTTPStatus
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_db
from src.schemas.transaction_schema import TransactionRequest
from src.services.transaction_service import TransactionService


router=APIRouter(prefix="/transactions",tags=["transactions"])

@router.post("/",status_code=HTTPStatus.CREATED)
async def create_transaction(transaction: TransactionRequest, db: AsyncSession = Depends(get_db)):
    return await TransactionService(db).create_transaction(transaction)


@router.get("/transactions/detail/{transaction_id}")
async def get_transaction_detail(transaction_id: int, db: AsyncSession = Depends(get_db)):
    return await TransactionService(db).get_transaction_detail(transaction_id)


# GET /transactions/{user_id}?page=1&limit=10
@router.get("/transactions/{user_id}")
async def get_user_transactions(user_id: int, db: AsyncSession = Depends(get_db), page: int = 1, limit: int = 10):
    return await TransactionService(db).get_user_transactions(user_id, page, limit)