from typing import List, Any

from sqlalchemy.orm import Session, selectinload
from app.orders.model import Order, OrderItem, OrderStatus
from app.products.model import Product
from app.orders.schema import OrderCreate
from app.users.model import Customer
from fastapi import HTTPException

def create_order(db: Session, order_in: OrderCreate):
    customer = db.query(Customer).get(order_in.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    product_ids = [item.product_id for item in order_in.items]
    products = db.query(Product).filter(Product.id.in_(product_ids)).all()

    if len(products) != len(order_in.items):
        raise HTTPException(status_code=404, detail="One or more products not found")

    # Check inventory
    for item in order_in.items:
        product = next((p for p in products if p.id == item.product_id), None)
        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product '{product.name}'"
            )

    # Create order
    order = Order(customer_id=order_in.customer_id)
    db.add(order)
    db.commit()
    db.refresh(order)

    # Add items to order and update inventory
    for item in order_in.items:
        product = next(p for p in products if p.id == item.product_id)
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_order=product.price
        )
        db.add(order_item)
        product.stock_quantity -= item.quantity

    db.commit()
    db.refresh(order)
    return order

def get_order(db: Session, order_id: int):
    order = db.query(Order).get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def get_all_orders(db: Session):
    return db.query(Order).options(selectinload(Order.items)).all()

def get_orders_by_customer(db: Session, customer_id: int) -> list[type[Order]]:
    return db.query(Order).filter(Order.customer_id == customer_id).all()

def get_orders_by_status(db: Session, status: OrderStatus) -> list[type[Order]]:
    return db.query(Order).filter(Order.status == status).all()

def get_orders_by_status_for_customer(db: Session, customer_id: int, status: OrderStatus) -> list[type[Order]]:
    return db.query(Order).filter(Order.customer_id == customer_id, Order.status == status).all()
def update_order_status(db: Session, order_id: int, status: OrderStatus):
    order = db.query(Order).get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    db.commit()
    db.refresh(order)
    return order

def cancel_order(db: Session, order_id: int):
    order = db.query(Order).get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status == OrderStatus.cancelled:
        raise HTTPException(status_code=400, detail="Order is already cancelled")

    # Restore inventory
    for item in order.items:
        item.product.stock_quantity += item.quantity

    order.status = OrderStatus.cancelled
    db.commit()
    db.refresh(order)
    return order
