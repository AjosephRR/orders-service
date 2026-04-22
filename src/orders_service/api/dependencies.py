from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from orders_service.infrastructure.database.session import SessionLocal
from orders_service.infrastructure.repositories.sqlalchemy_order_repository import (
    SqlAlchemyOrderRepository,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_repository(db: Session = Depends(get_db)):
    return SqlAlchemyOrderRepository(db)
