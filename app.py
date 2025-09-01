from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.db.db import Base, dbengine
from src.models import *
from src.routers.user_router import router as user_router
from src.routers.wallet_router import router as wallet_router
from src.routers.transfer_router import router as transfer_router
from src.routers.transaction_router import router as transaction_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with dbengine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield

app=FastAPI(title="User Management System",lifespan=lifespan)


app.include_router(user_router)
app.include_router(wallet_router)
app.include_router(transaction_router)
app.include_router(transfer_router)
 


@app.get("/health")
def read_root():
    return {"status": "healthy","success": True}