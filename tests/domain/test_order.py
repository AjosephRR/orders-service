from decimal import Decimal

import pytest

from orders_service.domain.entities.order import Order
from orders_service.domain.exceptions.domain_exceptions import (
    InvalidOrderStateTransitionError,
)
from orders_service.domain.value_objects.money import Money
from orders_service.domain.value_objects.order_id import OrderId
from orders_service.domain.value_objects.order_status import OrderStatus


def create_order() -> Order:
    return Order(id=OrderId.new(), total=Money(Decimal("100.00")))


def test_order_inicia_en_pending() -> None:
    order = create_order()
    assert order.status == OrderStatus.PENDING


def test_mark_as_paid_desde_pending() -> None:
    order = create_order()
    order.mark_as_paid()
    assert order.status == OrderStatus.PAID


def test_mark_as_paid_es_idempotente() -> None:
    order = create_order()
    order.mark_as_paid()
    order.mark_as_paid()
    assert order.status == OrderStatus.PAID


def test_mark_as_paid_falla_desde_shipped() -> None:
    order = create_order()
    order.mark_as_paid()
    order.ship()

    with pytest.raises(InvalidOrderStateTransitionError) as exc_info:
        order.mark_as_paid()

    assert str(exc_info.value) == (
        "No se puede pagar una orden en estado OrderStatus.SHIPPED."
    )


def test_ship_solo_desde_paid() -> None:
    order = create_order()
    with pytest.raises(InvalidOrderStateTransitionError):
        order.ship()

    order.mark_as_paid()
    order.ship()
    assert order.status == OrderStatus.SHIPPED


def test_no_se_puede_cancelar_orden_enviada() -> None:
    order = create_order()
    order.mark_as_paid()
    order.ship()

    with pytest.raises(InvalidOrderStateTransitionError):
        order.cancel()


def test_cancel_desde_pending() -> None:
    order = create_order()
    order.cancel()
    assert order.status == OrderStatus.CANCELLED
