import os
from pathlib import Path

import bcrypt
from sqlalchemy import create_engine

TEST_AUTH_USERNAME = "admin"
TEST_AUTH_PASSWORD = "admin-test-password"
TEST_DATABASE_PATH = Path("test_orders.db")

if TEST_DATABASE_PATH.exists():
    TEST_DATABASE_PATH.unlink()

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
os.environ.setdefault("DATABASE_URL", f"sqlite:///./{TEST_DATABASE_PATH}")
os.environ.setdefault("DB_ECHO", "false")


def _initialize_test_database() -> None:
    from orders_service.infrastructure.database import models  # noqa: F401
    from orders_service.infrastructure.database.base import Base

    engine = create_engine(os.environ["DATABASE_URL"])
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


_initialize_test_database()
