import uuid
from fastapi.testclient import TestClient
from orders_service.api.main import app

client = TestClient(app)


def test_create_order_endpoint():
    response = client.post("/orders/", json={"total": 123.45})

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == "123.45"
    assert data["status"] == "PENDING"


def test_get_order_invalid_uuid():
    response = client.get("/orders/not-a-valid-uuid")
    assert response.status_code == 422


def test_get_order_not_found_valid_uuid():
    fake_id = str(uuid.uuid4())
    response = client.get(f"/orders/{fake_id}")
    assert response.status_code == 404


def test_get_order_success():
    create_response = client.post("/orders/", json={"total": 50})
    order_id = create_response.json()["id"]

    response = client.get(f"/orders/{order_id}")

    assert response.status_code == 200
    assert response.json()["id"] == order_id
