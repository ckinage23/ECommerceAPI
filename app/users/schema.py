from pydantic import BaseModel, EmailStr
from typing import Optional
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"

class CustomerBase(BaseModel):
    name: Optional[str]
    email: EmailStr
    phone: Optional[str]


class CustomerCreate(CustomerBase):
    oauth_provider: Optional[str] = None
    oauth_sub: Optional[str] = None
    password: Optional[str] # optional, if using email/password fallback
    role: UserRole = UserRole.CUSTOMER


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None

class CustomerOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    role: UserRole = UserRole.CUSTOMER

    class Config:
        from_attributes = True

class CustomerDeleteOut(BaseModel):
    message: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str

    class Config:
        from_attributes = True


class CustomerRoleUpdate(BaseModel):
    role: UserRole