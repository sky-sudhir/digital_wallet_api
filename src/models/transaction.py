from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import relationship

from src.db.db import Base

from sqlalchemy import Integer

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transaction_type = Column(String(20), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(Text, nullable=True)
    reference_transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)
    recipient_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(TIMESTAMP, default=func.now())
    user = relationship("User", back_populates="transactions", foreign_keys=[user_id])