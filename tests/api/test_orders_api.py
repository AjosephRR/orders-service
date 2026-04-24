import uuid

from fastapi.testclient import TestClient

from orders_service.api.main import app
from tests.conftest import TEST_AUTH_PASSWORD, TEST_AUTH_USERNAME

client = TestClient(app)


def get_auth_token() -> str:
    response = client.post(
        "/auth/login",
        json={"username": TEST_AUTH_USERNAME, "password": TEST_AUTH_PASSWORD},
    )
    return response.json()["access_token"]


def test_create_order_endpoint():
    token = get_auth_token()

    response = client.post(
        "/orders/",
        json={"total": 123.45},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200


def test_get_order_success():
    token = get_auth_token()

    create_response = client.post(
        "/orders/",
        json={"total": 50},
        headers={"Authorization": f"Bearer {token}"},
    )

    order_id = create_response.json()["id"]

    response = client.get(
        f"/orders/{order_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200


def test_get_order_invalid_uuid():
    token = get_auth_token()

    response = client.get(
        "/orders/not-a-valid-uuid",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422


def test_get_order_not_found_valid_uuid():
    token = get_auth_token()
    fake_id = str(uuid.uuid4())

    response = client.get(
        f"/orders/{fake_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


def test_healthcheck_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_process_time_header_is_present():
    response = client.get("/health")

    assert response.status_code == 200
    assert "X-Process-Time" in response.headers
    assert float(response.headers["X-Process-Time"]) >= 0
