from sqlalchemy import Column, Integer, BigInteger, Text, DateTime, Boolean
from .base import Base
from datetime import datetime

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    task_text = Column(Text, nullable=False)
    deadline = Column(Text, nullable=False)  # ISO формат, например '2025-02-14T18:00:00'
    is_done = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.now)