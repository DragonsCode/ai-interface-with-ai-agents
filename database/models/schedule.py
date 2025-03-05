from sqlalchemy import Column, Integer, BigInteger, Text, DateTime
from .base import Base
from datetime import datetime

class Schedule(Base):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    event_text = Column(Text, nullable=False)
    event_datetime = Column(Text, nullable=False)  # ISO формат, например '2025-02-14T15:00:00'
    timestamp = Column(DateTime, default=datetime.now)