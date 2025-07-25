# scripts/create_admin.py
import sys
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.users.model import Customer
from app.auth.auth import hash_password
from app.users.model import UserRole

def create_admin():
    db: Session = SessionLocal()

    email = "admin@example.com"
    phone = "9999888823"
    existing = db.query(Customer).filter(Customer.email == email).first()
    if existing:
        print("Admin user already exists.")
        return

    admin = Customer(
        name = "Admin",
        email = email,
        phone = phone,
        oauth_provider = None,
        oauth_sub = None,
        hashed_password = hash_password("securepassword"),
        role=UserRole.ADMIN
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)
    print("✅ Admin user created.")

if __name__ == "__main__":
    create_admin()
