from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.products.model import Product
from app.products.schema import ProductCreate

def get_all_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_products_by_category(db: Session, category_id: int):
    return db.query(Product).filter(Product.category_id == category_id).all()

def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    try:
        db.commit()
        db.refresh(db_product)
        return db_product
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid category ID or product already exists")


def get_stock_quantity(db: Session, product_id: int) -> int | None:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    return product.stock_quantity

def update_stock_quantity(db: Session, product_id: int, delta: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        return None

    new_quantity = product.stock_quantity + delta

    if new_quantity < 0:
        return None

    product.stock_quantity = new_quantity
    db.commit()
    db.refresh(product)
    return product

def update_product_price(db: Session, product_id: int, new_price: float):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    product.price = new_price
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    db.delete(product)
    db.commit()
    return product
