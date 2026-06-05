from decimal import Decimal

import pytest

from orders_service.application.use_cases.create_order import CreateOrder
from orders_service.domain.exceptions.domain_exceptions import (
    InvalidOrderTotalError,
)
from orders_service.domain.value_objects.order_status import OrderStatus
from tests.application.fake_order_repository import InMemoryOrderRepository


def test_create_order_crea_y_guarda_orden() -> None:
    repository = InMemoryOrderRepository()
    use_case = CreateOrder(repository)

    order = use_case.execute(
        Decimal("100.00"),
        customer_name="Angel Rivera",
        customer_email="angelrivera@example.com",
        shipping_address="Calle Principal 123, CDMX",
        notes="Entregar en horario matutino.",
    )

    assert order is not None
    assert order.status == OrderStatus.PENDING
    assert order.customer_name == "Angel Rivera"
    assert order.customer_email == "angelrivera@example.com"
    assert order.shipping_address == "Calle Principal 123, CDMX"
    assert order.notes == "Entregar en horario matutino."
    stored = repository.get_by_id(order.id)
    assert stored is not None
    assert stored.id == order.id
    assert stored.total.amount == Decimal("100.00")
    assert stored.customer_name == "Angel Rivera"
    assert stored.customer_email == "angelrivera@example.com"
    assert stored.shipping_address == "Calle Principal 123, CDMX"
    assert stored.notes == "Entregar en horario matutino."


def test_create_order_con_total_invalido_no_guarda() -> None:
    repository = InMemoryOrderRepository()
    use_case = CreateOrder(repository)

    with pytest.raises(InvalidOrderTotalError):
        use_case.execute(Decimal("-1.00"))
    assert repository._orders == {}
