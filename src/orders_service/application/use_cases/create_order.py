from decimal import Decimal

from orders_service.application.ports.order_repository import OrderRepository
from orders_service.domain.entities.order import Order
from orders_service.domain.value_objects.money import Money
from orders_service.domain.value_objects.order_id import OrderId


class CreateOrder:
    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    def execute(
        self,
        total: Decimal,
        customer_name: str | None = None,
        customer_email: str | None = None,
        shipping_address: str | None = None,
        notes: str | None = None,
    ) -> Order:
        order = Order(
            id=OrderId.new(),
            total=Money(total),
            customer_name=customer_name,
            customer_email=customer_email,
            shipping_address=shipping_address,
            notes=notes,
        )

        self._repository.save(order)

        return order
