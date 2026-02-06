from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from src.config import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("Products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Numeric(10,2), nullable=False)  

  
    order = relationship("Order", back_populates="items")
    product = relationship("Product")