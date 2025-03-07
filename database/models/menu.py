from sqlalchemy import Column, Integer, Text, Float, Boolean
from .base import Base

class Menu(Base):
    __tablename__ = "menu"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)