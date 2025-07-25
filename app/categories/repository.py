from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.categories.model import Category
from app.categories.schema import CategoryCreate, CategoryUpdate

def create_category(db: Session, category_in: CategoryCreate):
    existing = db.query(Category).filter(Category.name == category_in.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    category = Category(name=category_in.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_category(db: Session, category_id: int):
    category = db.query(Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

def get_all_categories(db: Session):
    return db.query(Category).all()

def update_category(db: Session, category_id: int, category_in: CategoryUpdate):
    category = db.query(Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.name = category_in.name
    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, category_id: int):
    category = db.query(Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"detail": "Category deleted successfully"}
