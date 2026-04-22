import pytest
from decimal import Decimal

from orders_service.domain.value_objects.money import Money
from orders_service.domain.exceptions.domain_exceptions import (
    InvalidOrderTotalError,
)


def test_money_normaliza_a_dos_decimales() -> None:
    money = Money(Decimal("10.567"))
    assert money.amount == Decimal("10.57")


def test_money_rechaza_valores_negativos() -> None:
    with pytest.raises(InvalidOrderTotalError):
        Money(Decimal("-1.00"))
