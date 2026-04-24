import os

import bcrypt

TEST_AUTH_USERNAME = "admin"
TEST_AUTH_PASSWORD = "admin-test-password"

os.environ.setdefault(
    "SECRET_KEY",
    "test-secret-key-for-orders-service-32-chars",
)
os.environ.setdefault("AUTH_USERNAME", TEST_AUTH_USERNAME)
os.environ.setdefault(
    "AUTH_PASSWORD_HASH",
    bcrypt.hashpw(
        TEST_AUTH_PASSWORD.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8"),
)
os.environ.setdefault("DATABASE_URL", "sqlite:///./orders.db")
os.environ.setdefault("DB_ECHO", "false")
