from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import DATABASE_URL


class Base(DeclarativeBase):
    pass


dbengine=create_async_engine(DATABASE_URL,echo=True,future=True)

AsyncLocalEngine=async_sessionmaker(dbengine, expire_on_commit=False)

async def get_db():
    async with AsyncLocalEngine() as session:
        yield session