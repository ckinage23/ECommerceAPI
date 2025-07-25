from fastapi import APIRouter, Depends
from fastapi.params import Body, Query
from sqlalchemy.orm import Session
from fastapi_pagination import Page, paginate
from app.dependencies.deps import get_db
from app.orders.schema import OrderCreate, OrderOut, OrderStatus
import app.orders.repository as order_crud
from app.auth.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])

@router.get("/", response_model=Page[OrderOut])
def read_all_orders(db: Session = Depends(get_db), user=Depends(require_admin)):
    return paginate(order_crud.get_all_orders(db))

@router.get("/me", response_model=Page[OrderOut])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    orders = order_crud.get_orders_by_customer(db=db, customer_id=current_user.id)
    return paginate(orders)

@router.get("/by-status", response_model=Page[OrderOut])
def get_all_orders_by_status(
    status: OrderStatus = Query(..., description="Filter by order status"),
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    return paginate(order_crud.get_orders_by_status(db=db, status=status))


@router.get("/me/by-status", response_model=Page[OrderOut])
def get_my_orders_by_status(
    status: OrderStatus = Query(..., description="Filter by your order status"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return paginate(order_crud.get_orders_by_status_for_customer(
        db=db, customer_id=current_user.id, status=status
    ))
@router.post("/", response_model=OrderOut)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return order_crud.create_order(db, order_in)



@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    return order_crud.get_order(db, order_id)

@router.put("/{order_id}/status", response_model=OrderOut)
def update_status(order_id: int, status: OrderStatus = Body(...), db: Session = Depends(get_db), user=Depends(require_admin)):
    return order_crud.update_order_status(db, order_id, status)

@router.put("/{order_id}/cancel", response_model=OrderOut)
def cancel_order(order_id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    return order_crud.cancel_order(db, order_id)
