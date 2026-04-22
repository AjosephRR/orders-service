from dataclasses import dataclass, field
from datetime import datetime

from orders_service.domain.exceptions.domain_exceptions import (
    InvalidOrderStateTransitionError,
)
from orders_service.domain.value_objects.money import Money
from orders_service.domain.value_objects.order_id import OrderId
from orders_service.domain.value_objects.order_status import OrderStatus
from datetime import datetime, UTC


@dataclass
class Order:
    id: OrderId
    total: Money
    status: OrderStatus = field(default=OrderStatus.PENDING)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def mark_as_paid(self) -> None:
        if self.status == OrderStatus.PAID:
            return  # idempotente

        if self.status != OrderStatus.PENDING:
            raise InvalidOrderStateTransitionError(
                f"No se puede pagar una orden en estado {self.status}."
            )

        self.status = OrderStatus.PAID

    def ship(self) -> None:
        if self.status != OrderStatus.PAID:
            raise InvalidOrderStateTransitionError(
                "Solo se pueden enviar órdenes pagadas."
            )

        self.status = OrderStatus.SHIPPED

    def cancel(self) -> None:
        if self.status in {OrderStatus.SHIPPED, OrderStatus.CANCELLED}:
            raise InvalidOrderStateTransitionError(
                f"No se puede cancelar una orden en estado {self.status}."
            )

        self.status = OrderStatus.CANCELLED
