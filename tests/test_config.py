import bcrypt
import pytest
from pydantic import ValidationError

from orders_service.config import Settings


def test_settings_reject_short_secret_key():
    valid_hash = bcrypt.hashpw(b"config-password", bcrypt.gensalt()).decode("utf-8")

    with pytest.raises(ValidationError):
        Settings(
            secret_key="short-secret",
            auth_username="config-user",
            auth_password_hash=valid_hash,
        )


def test_settings_reject_invalid_bcrypt_hash():
    with pytest.raises(ValidationError):
        Settings(
            secret_key="this-secret-key-has-more-than-32-chars",
            auth_username="config-user",
            auth_password_hash="not-a-valid-bcrypt-hash",
        )
