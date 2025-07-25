from sqlalchemy.orm import Session
from app.users.model import Customer, UserRole
from app.users.schema import CustomerCreate, CustomerUpdate
from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_customer(db: Session, customer_in: CustomerCreate) -> Customer:
    db_customer = db.query(Customer).filter(Customer.email == customer_in.email).first()
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = (
        pwd_context.hash(customer_in.password) if customer_in.password else None
    )

    new_customer = Customer(
        name=customer_in.name,
        email=customer_in.email,
        phone=customer_in.phone,
        oauth_provider=customer_in.oauth_provider,
        oauth_sub=customer_in.oauth_sub,
        hashed_password=hashed_password,
        role=UserRole.CUSTOMER
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


def get_customer(db: Session, customer_id: int) -> Customer:
    customer = db.query(Customer).get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

def get_customer_by_email(db: Session, email: str) -> Customer | None:
    return db.query(Customer).filter(Customer.email == email).first()

def get_all_customers(db: Session):
    return db.query(Customer).all()

def update_customer(db: Session, customer_id: int, update_data: CustomerUpdate) -> Customer:
    customer = get_customer(db, customer_id)

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)
    return customer

def update_customer_role(db: Session, customer_id: int, new_role: UserRole):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return None
    customer.role = new_role
    db.commit()
    db.refresh(customer)
    return customer

def delete_customer(db: Session, customer_id: int):
    customer = db.query(Customer).get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(customer)
    db.commit()
    return {"message": f"Customer with ID {customer_id} has been deleted."}

