from typing import Annotated, Generator

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from orders_service.api.security import verify_token
from orders_service.application.ports.order_repository import OrderRepository
from orders_service.infrastructure.database.session import SessionLocal
from orders_service.infrastructure.repositories.sqlalchemy_order_repository import (
    SqlAlchemyOrderRepository,
)

security = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_repository(
    db: Annotated[Session, Depends(get_db)],
) -> OrderRepository:
    return SqlAlchemyOrderRepository(db)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> str:
    token = credentials.credentials
    try:
        payload = verify_token(token)
        sub = payload.get("sub")

        if not isinstance(sub, str) or not sub:
            raise HTTPException(status_code=401, detail="Invalid token")

        return sub

    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
