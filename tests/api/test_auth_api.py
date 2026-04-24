import jwt
from fastapi.testclient import TestClient
from pydantic import SecretStr

from orders_service.api.main import app
from orders_service.config import settings
from tests.conftest import TEST_AUTH_PASSWORD, TEST_AUTH_USERNAME

client = TestClient(app)


def get_auth_token() -> str:
    response = client.post(
        "/auth/login",
        json={"username": TEST_AUTH_USERNAME, "password": TEST_AUTH_PASSWORD},
    )
    return response.json()["access_token"]


def test_login_success():
    response = client.post(
        "/auth/login",
        json={"username": TEST_AUTH_USERNAME, "password": TEST_AUTH_PASSWORD},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_access_without_token():
    response = client.post("/orders/", json={"total": 10})
    assert response.status_code == 401


def test_login_invalid_credentials():
    response = client.post(
        "/auth/login",
        json={"username": TEST_AUTH_USERNAME, "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_access_with_invalid_token():
    response = client.post(
        "/orders/",
        json={"total": 10},
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert response.status_code == 401


def test_token_without_sub():
    token = jwt.encode(
        {"foo": "bar"},
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm,
    )

    response = client.post(
        "/orders/",
        json={"total": 10},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401


def test_create_order_invalid_total_authenticated():
    token = get_auth_token()

    response = client.post(
        "/orders/",
        json={"total": -10},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422


def test_login_handles_invalid_password_hash_configuration(monkeypatch):
    original_hash = settings.auth_password_hash
    monkeypatch.setattr(settings, "auth_password_hash", SecretStr("invalid-hash"))

    response = client.post(
        "/auth/login",
        json={"username": TEST_AUTH_USERNAME, "password": TEST_AUTH_PASSWORD},
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "Authentication is not configured correctly."}

    monkeypatch.setattr(settings, "auth_password_hash", original_hash)
