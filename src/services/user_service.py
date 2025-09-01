from fastapi import HTTPException
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.schemas.user_schema import UpdateUser, UserCreate


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users(self):
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def create_user(self, user: UserCreate):
        existing_user = await self.session.execute(
            select(User).where(User.email == user.email)
        )

        if existing_user.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="User with this email already exists.")

        new_user = User(**user.model_dump())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
    
    async def get_user_by_id(self, user_id: int):
        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        
        return user

    async def update_user(self, user_id: int, user_data: UpdateUser):
        user = await self.get_user_by_id(user_id)
        for key, value in user_data.model_dump().items():
            setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user