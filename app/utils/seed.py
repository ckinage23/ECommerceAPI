# app/utils/seed.py

from faker import Faker
from sqlalchemy.orm import Session
from app.users.model import Customer
from app.categories.model import Category
from app.products.model import Product
from app.orders.model import Order, OrderItem
from app.db.session import SessionLocal

import random

fake = Faker()

def seed_data(db: Session):
    # Create categories
    categories = []
    for _ in range(5):
        category = Category(name=fake.word())
        db.add(category)
        categories.append(category)
    db.commit()

    # Create products
    products = []
    for _ in range(20):
        product = Product(
            name=fake.unique.word().title(),
            description=fake.text(max_nb_chars=50),
            price=round(random.uniform(10.0, 500.0), 2),
            stock_quantity=random.randint(10, 100),
            category_id=random.choice(categories).id,
        )
        db.add(product)
        products.append(product)
    db.commit()

    # Create users
    customers = []
    for _ in range(10):
        customer = Customer(
            name=fake.name(),
            email=fake.unique.email(),
            hashed_password="not_really_hashed",  # Replace with real hash if needed
        )
        db.add(customer)
        customers.append(customer)
    db.commit()

    # Create orders
    for _ in range(10):
        customer = random.choice(customers)
        order = Order(customer_id=customer.id, status="pending")
        db.add(order)
        db.commit()
        db.refresh(order)

        # Add order items
        for _ in range(random.randint(1, 5)):
            product = random.choice(products)
            stock_quantity = random.randint(1, 3)

            # Check stock
            if product.stock_quantity >= stock_quantity:
                product.stock_quantity -= stock_quantity
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=stock_quantity,
                    price_at_order=product.price,
                )
                db.add(order_item)
        db.commit()

    print("✅ Seed data created.")

if __name__ == "__main__":
    db = SessionLocal()
    seed_data(db)
    db.close()
