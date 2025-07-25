from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.users import schema, repositoy
from app.dependencies.deps import get_db
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/customer", tags=["Customers"])

@router.get("/me", response_model=schema.UserOut)
def get_my_profile(current_user: schema.UserOut = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=schema.UserOut)
def update_my_profile(
    user_update: schema.CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: schema.UserOut = Depends(get_current_user),
):
    return repositoy.update_customer(db=db, customer_id=current_user.id, update_data=user_update)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_account(
    db: Session = Depends(get_db),
    current_user: schema.UserOut = Depends(get_current_user),
):
    repositoy.delete_customer(db, current_user.id)
