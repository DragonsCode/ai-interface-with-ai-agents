from sqlalchemy import Column, Integer, BigInteger, DateTime
from .base import Base
from datetime import datetime

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)