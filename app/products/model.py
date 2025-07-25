from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    stock_quantity = Column(Integer, default=0)  # 📦 inventory tracking

    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False) # 🔗 FK to category

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
