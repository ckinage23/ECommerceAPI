from fastapi.testclient import TestClient
from app.main import app
from tests.utils import login_and_get_token
client = TestClient(app)

def test_create_order_with_insufficient_stock():
    token = login_and_get_token()  # helper
    response = client.post(
        "/api/v1/orders/",
        json={
            "customer_id": 3,
            "items": [
                {"product_id": 1, "quantity": 9999}
            ]
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert "insufficient stock" in response.text.lower()
