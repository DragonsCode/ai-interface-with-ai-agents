from sqlalchemy import Column, Integer, BigInteger, Text, DateTime
from .base import Base
from datetime import datetime

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    note_text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)