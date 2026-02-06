from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from src.config import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    total_price = Column(Numeric(10,2), nullable=False, default=0)
    status = Column(String(50), default="pending")  

  
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")