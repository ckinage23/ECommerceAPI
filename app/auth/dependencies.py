from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from app.auth.auth import SECRET_KEY, ALGORITHM
from app.auth.schema import TokenData
from app.dependencies.deps import get_db
from sqlalchemy.orm import Session
from app.users import repositoy as customer_repo
from app.users.schema import UserOut

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = customer_repo.get_customer_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

def require_admin(user: UserOut = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action"
        )
    return user


def require_customer(user: UserOut = Depends(get_current_user)):
    if user.role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be a customer to access this route"
        )
    return user
