from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.deps import get_db
from app.categories.schema import CategoryCreate, CategoryUpdate, CategoryOut
import app.categories.repository as category_crud
from app.auth.dependencies import  require_admin
from fastapi_pagination import Page, paginate

router = APIRouter(prefix="/api/v1/categories", tags=["Categories"])

@router.post("/", response_model=CategoryOut)
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db), user=Depends(require_admin)):
    return category_crud.create_category(db, category_in)

@router.get("/", response_model=Page[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return paginate(category_crud.get_all_categories(db))

@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    return category_crud.get_category(db, category_id)

@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, category_in: CategoryUpdate, db: Session = Depends(get_db), user=Depends(require_admin)):
    return category_crud.update_category(db, category_id, category_in)

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    return category_crud.delete_category(db, category_id)
