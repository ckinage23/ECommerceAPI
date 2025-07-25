from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"

class Customer(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # Basic profile info
    name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=True)

    # OAuth-related fields
    oauth_provider = Column(String, nullable=True)  # e.g., 'google', 'github'
    oauth_sub = Column(String, nullable=True)  # unique ID from provider
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)

    # Optional fallback for local auth
    hashed_password = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)

    # One-to-many: one customer can have multiple orders
    orders = relationship("Order", back_populates="customer", cascade="all, delete")
