from decimal import Decimal

from orders_service.domain.entities.order import Order
from orders_service.domain.value_objects.money import Money
from orders_service.domain.value_objects.order_id import OrderId
from orders_service.application.ports.order_repository import OrderRepository


class CreateOrder:

    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    def execute(self, total: Decimal) -> Order:
        order = Order(
            id=OrderId.new(),
            total=Money(total),
        )

        self._repository.save(order)

        return order
