from fastapi.testclient import TestClient
from app.main import app
from tests.utils import login_as_admin
client = TestClient(app)
token = login_as_admin()

def test_register_user_with_existing_email():
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "c.doe@example.com",  # already exists
            "password": "StrongPassword123",
            "name": "Duplicate User",
            "phone": "8888710134"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert "email already registered" in response.text.lower()

