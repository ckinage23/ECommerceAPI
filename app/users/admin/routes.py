from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.users.model import Customer
from app.users.schema import CustomerCreate, CustomerOut, CustomerUpdate, CustomerDeleteOut, CustomerRoleUpdate
from app.dependencies.deps import get_db
import app.users.repositoy as customer_crud
from app.auth.dependencies import require_admin
from fastapi_pagination import Page, paginate

router = APIRouter(prefix="/api/v1/users", tags=["Customers"])

@router.get("/", response_model=Page[CustomerOut])
def get_all_customers(db: Session = Depends(get_db), user=Depends(require_admin)):
    return paginate(customer_crud.get_all_customers(db))

@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    return customer_crud.get_customer(db, customer_id)

@router.get("/by-email", response_model=CustomerOut)
def get_customer_by_email(email: str = Query(...), db: Session = Depends(get_db), user=Depends(require_admin)):
    customer = customer_crud.get_customer_by_email(db, email)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/", response_model=CustomerOut)
def create_customer(customer_in: CustomerCreate, db: Session = Depends(get_db), user=Depends(require_admin)):
    return customer_crud.create_customer(db, customer_in)


@router.patch("/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, customer_update: CustomerUpdate, db: Session = Depends(get_db), user=Depends(require_admin)):
    return customer_crud.update_customer(db, customer_id, customer_update)

@router.put("/{customer_id}/role", response_model=CustomerOut)
def change_customer_role(
    customer_id: int,
    role_data: CustomerRoleUpdate,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(require_admin),  # ✅ only admin can access
):
    updated = customer_crud.update_customer_role(db, customer_id, role_data.role)
    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated
@router.delete("/{customer_id}", response_model=CustomerDeleteOut)
def delete_customer(customer_id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    return customer_crud.delete_customer(db, customer_id)
