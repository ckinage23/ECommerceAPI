from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def login_as_admin(email="admin@example.com", password="securepassword"):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json()["access_token"]

def login_and_get_token(email="c.doe@example.com", password="StrongPassword123"):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json()["access_token"]

