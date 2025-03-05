from sqlalchemy import Column, Integer, Text, ForeignKey
from .base import Base

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    item_name = Column(Text, nullable=False)
    quantity = Column(Integer, nullable=False)