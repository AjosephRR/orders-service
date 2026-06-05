from datetime import UTC
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from orders_service.application.ports.order_repository import OrderRepository
from orders_service.domain.entities.order import Order
from orders_service.domain.value_objects.money import Money
from orders_service.domain.value_objects.order_id import OrderId
from orders_service.domain.value_objects.order_status import OrderStatus
from orders_service.infrastructure.database.models import OrderModel


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, order: Order) -> None:
        model = OrderModel(
            id=str(order.id),
            total=order.total.amount,
            customer_name=order.customer_name,
            customer_email=order.customer_email,
            shipping_address=order.shipping_address,
            notes=order.notes,
            status=order.status.value,
            created_at=order.created_at,
        )

        self._session.merge(model)
        self._session.commit()

    def get_by_id(self, order_id: OrderId) -> Order | None:
        model = self._session.get(OrderModel, str(order_id))

        if model is None:
            return None

        return Order(
            id=OrderId(UUID(str(model.id))),
            total=Money(Decimal(model.total)),
            customer_name=model.customer_name,
            customer_email=model.customer_email,
            shipping_address=model.shipping_address,
            notes=model.notes,
            status=OrderStatus(model.status),
            created_at=model.created_at.replace(tzinfo=UTC),
        )
