from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from app.auth.schema import LoginRequest, Token
from app.dependencies.deps import get_db
from app.auth.auth import verify_password, create_access_token
from app.users import repositoy as customers_repo

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = customers_repo.get_customer_by_email(db, email=request.email)
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=timedelta(minutes=60)
    )
    return {"access_token": access_token, "role": user.role, "token_type": "bearer"}
