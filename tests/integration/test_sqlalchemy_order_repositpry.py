from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orders_service.domain.entities.order import Order
from orders_service.domain.value_objects.money import Money
from orders_service.domain.value_objects.order_id import OrderId
from orders_service.infrastructure.database.base import Base
from orders_service.infrastructure.repositories.sqlalchemy_order_repository import (
    SqlAlchemyOrderRepository,
)


def test_sqlalchemy_repository_save_and_get() -> None:
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(bind=engine)

    repository = SqlAlchemyOrderRepository(session)

    order = Order(
        id=OrderId.new(),
        total=Money(Decimal("150.00")),
    )

    repository.save(order)

    retrieved = repository.get_by_id(order.id)

    assert retrieved is not None
    assert retrieved.id == order.id
    assert retrieved.total.amount == Decimal("150.00")
    assert retrieved.status == order.status
    assert retrieved.created_at == order.created_at
