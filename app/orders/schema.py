from pydantic import BaseModel
from typing import List
from enum import Enum


class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


# Schema to represent an item in the order (used for create input)
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


# Input schema for creating an order
class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]


# Schema for returning item in the order (used in OrderOut)
class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


# Output schema for returning order details
class OrderOut(BaseModel):
    id: int
    customer_id: int
    status: OrderStatus
    items: List[OrderItemOut]

    class Config:
        from_attributes = True
