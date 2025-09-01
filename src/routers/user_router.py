
from http import HTTPStatus
import stat
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_db
from src.schemas.user_schema import UpdateUser, UserCreate
from src.services.user_service import UserService


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def get_users(db:AsyncSession=Depends(get_db)):
    result=await UserService(db).get_users()
    return result

@router.post("/",status_code=HTTPStatus.CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await UserService(db).create_user(user)
    del result.password
    return result

@router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await UserService(db).get_user_by_id(user_id)
    del result.password
    return result

@router.put("/{user_id}")
async def update_user(user_id: int, user_data: UpdateUser, db: AsyncSession = Depends(get_db)):
    result = await UserService(db).update_user(user_id, user_data)
    del result.password
    return result