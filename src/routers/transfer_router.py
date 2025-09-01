from http import HTTPStatus
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_db
from src.schemas.transfer_schema import TransferRequest
from src.services.transfer_service import TransferService


router = APIRouter(prefix="/transfer",tags=["transfer"])

@router.post("/", status_code=HTTPStatus.CREATED)
async def create_transfer(transfer_request: TransferRequest, db: AsyncSession = Depends(get_db)):
    service = TransferService(db)
    new_transaction = await service.transfer_money(transfer_request)
    return new_transaction

@router.get("/{transfer_id}")
async def get_transfer(transfer_id: int, db: AsyncSession = Depends(get_db)):
    service = TransferService(db)
    transaction = await service.get_transfer_detail(transfer_id)
    return transaction