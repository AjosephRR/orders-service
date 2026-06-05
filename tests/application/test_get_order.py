from decimal import Decimal

import pytest

from orders_service.application.exceptions import OrderNotFoundError
from orders_service.application.use_cases.get_order import GetOrder
from orders_service.domain.entities.order import Order
from orders_service.domain.value_objects.money import Money
from orders_service.domain.value_objects.order_id import OrderId
from tests.application.fake_order_repository import InMemoryOrderRepository


def test_get_order_retorna_orden_existente() -> None:
    repository = InMemoryOrderRepository()
    order = Order(
        id=OrderId.new(),
        total=Money(Decimal("50.00")),
        customer_name="Angel Rivera",
        customer_email="angelrivera@example.com",
        shipping_address="Calle Principal 123, CDMX",
        notes="Entregar en horario matutino.",
    )
    repository.save(order)

    use_case = GetOrder(repository)

    result = use_case.execute(order.id)

    assert result.id == order.id
    assert result.customer_name == "Angel Rivera"
    assert result.customer_email == "angelrivera@example.com"
    assert result.shipping_address == "Calle Principal 123, CDMX"
    assert result.notes == "Entregar en horario matutino."


def test_get_order_lanza_error_si_no_existe() -> None:
    repository = InMemoryOrderRepository()
    use_case = GetOrder(repository)

    with pytest.raises(OrderNotFoundError):
        use_case.execute(OrderId.new())
