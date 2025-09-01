from sqlalchemy import TIMESTAMP, Column, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from src.db.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(15), nullable=True)
    balance = Column(Numeric(10, 2), default=0.00)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    transactions = relationship("Transaction", back_populates="user", foreign_keys="[Transaction.user_id]")


