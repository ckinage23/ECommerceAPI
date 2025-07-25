from fastapi.testclient import TestClient
from app.main import app
from tests.utils import login_as_admin
client = TestClient(app)
token = login_as_admin()
def test_create_product_with_missing_fields():
    response = client.post(
        "/api/v1/products/",
        json={  # Missing required fields
            "name": "Faulty Product"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422  # Unprocessable Entity
def test_create_product_with_invalid_category():

    response = client.post(
        "/api/v1/products/",
        json={
            "name": "InvalidCat",
            "description": "Bad data",
            "price": 10.99,
            "stock_quantity": 5,
            "category_id": 999
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert "invalid category" in response.text.lower()
