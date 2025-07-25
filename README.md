
# 🛒 FastAPI eCommerce App

A modular, secure, and scalable **eCommerce backend** built with **FastAPI** using **Clean Architecture**, **PostgreSQL**, and **SQLAlchemy ORM**, with **OAuth2-based authentication**, **role-based access control**, and **full test coverage**.

---

## 🚀 Features

- 🔐 OAuth2 Authentication (JWT) with password hashing
- 👥 Role-based access control (Admin / Customer)
- ✅ OpenAPI / Swagger documentation
- 🧪 Unit and Integration tests using `pytest`
- 📄 Postman collection for testing all APIs
- ⚙️ Alembic for database migrations

---

## 📁 Project Structure (Clean Architecture)

```
Ecommerce/
├── alembic/                  # Alembic migrations for database schema
├── app/                      # Main application code
│   ├── auth/                 # Authentication & authorization logic
│   ├── categories/           # Category module (similar structure to orders)
│   ├── db/                   # Database setup (session, base class)
│   ├── dependencies/         # FastAPI dependencies (e.g., get_db)
│   ├── orders/               # Order management module
│   │   ├── __init__.py
│   │   ├── model.py          # SQLAlchemy models
│   │   ├── repository.py     # Database operations (CRUD)
│   │   ├── routes.py         # FastAPI routes
│   │   ├── schema.py         # Pydantic schemas
│   ├── products/             # Product module (similar structure to orders)
│   ├── users/                # User module (similar structure to orders)
│   ├── utils/                # Utility functions and helpers
│   └── main.py               # Entry point for FastAPI app
├── scripts/                  # Optional scripts (e.g., create_admin)
├── tests/                    # Test suite (unit/integration tests)
```

---

## 🧑‍💻 Prerequisites

- Python 3.10+
- PostgreSQL installed and running locally
- `virtualenv` or `venv` for Python environment

---

## ⚙️ Environment Setup

### 1. Clone the repo and set up virtual environment

```bash
git clone https://github.com/your-username/fastapi-ecommerce.git
cd fastapi-ecommerce

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Create PostgreSQL Database

Ensure PostgreSQL is running and create a database:

```sql
CREATE DATABASE ecommerce_db;
```

Update your `.env` file (or `app/core/config.py`) with:

```env
DATABASE_URL=postgresql://postgres:kinage@localhost:5433/ecommerce_db

```

---

### 4. Run Alembic Migrations

```bash
alembic upgrade head
```

---

### 5. Seed Sample Data (Optional)

```bash
python seed.py
```

---

### 6. Run the Application

```bash
uvicorn app.main:app --reload
```

Visit your app at: [http://localhost:8000](http://localhost:8000)

---

## 📘 API Documentation

- 🧾 **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- 📚 **Redoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔐 Authentication

- OAuth2 with JWT Tokens
- Use `/api/v1/auth/login` to get access token (POST)
- Use token in header for protected endpoints:

```http
Authorization: Bearer <access_token>
```

---

## 📫 Postman Collection

✅ Import the Postman collection and environment from the links below:

- 🔗 [Postman Collection](https://www.postman.com/your-username/workspace/fastapi-ecommerce/collection/your-postman-id)
- 🔗 [Postman Environment](https://www.postman.com/your-username/workspace/fastapi-ecommerce/environment/your-env-id)

---

## 🧪 Running Tests

### 1. Run All Tests

```bash
pytest
````

### 2. Ignore Warnings

```bash
pytest -p no:warnings
```

### 3. Sample Tests Covered

- ✅ Product creation with invalid category ID
- ✅ Order placement with insufficient stock
- ✅ Role-based access (admin/customer)
- ✅ Edge cases like duplicate emails 

---


