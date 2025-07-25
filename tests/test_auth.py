from fastapi.testclient import TestClient
from app.main import app
from tests.utils import login_and_get_token
client = TestClient(app)
token = login_and_get_token()  # helper


def test_create_order_without_login():
    response = client.post(
        "/api/v1/orders/",
        json={
            "customer_id": 3,
            "items": [
                {"product_id": 1, "quantity": 6}
            ]
        }
    )
    assert response.status_code == 401
    assert "not authenticated" in response.text.lower()

def test_create_product_on_customer_login():
    response = client.post(
        "/api/v1/products/",
        json={
            "name": "InvalidCat",
            "description": "Bad data",
            "price": 10.99,
            "stock_quantity": 5,
            "category_id": 2
        },
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    assert "you are not authorized to perform this action" in response.text.lower()
