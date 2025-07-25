from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.products.schema import ProductCreate, ProductOut, ProductPriceUpdate
import app.products.repository as product_repo
from app.dependencies.deps import get_db
from app.auth.dependencies import require_admin
from fastapi_pagination import Page, paginate
router = APIRouter(prefix="/api/v1/products", tags=["Products"])

@router.get("/", response_model=Page[ProductOut])
def get_products(db: Session = Depends(get_db)):
    return paginate(product_repo.get_all_products(db))

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_repo.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/by-category/{category_id}", response_model=Page[ProductOut])
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    products = product_repo.get_products_by_category(db, category_id)
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this category")
    return paginate(products)

@router.get("/{product_id}/stock", response_model=int)
def check_stock(product_id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    stock = product_repo.get_stock_quantity(db, product_id)
    if stock is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return stock

@router.post("/", response_model=ProductOut, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db), user=Depends(require_admin)):
    return product_repo.create_product(db, product)

@router.put("/{product_id}/price", response_model=ProductOut)
def update_price(product_id: int, update: ProductPriceUpdate, db: Session = Depends(get_db), user=Depends(require_admin)):
    product = product_repo.update_product_price(db, product_id, update.price)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    deleted = product_repo.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
