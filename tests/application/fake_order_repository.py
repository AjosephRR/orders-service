from typing import Dict

from orders_service.application.ports.order_repository import OrderRepository
from orders_service.domain.entities.order import Order
from orders_service.domain.value_objects.order_id import OrderId


class InMemoryOrderRepository(OrderRepository):
    def __init__(self) -> None:
        self._orders: Dict[str, Order] = {}

    def save(self, order: Order) -> None:
        self._orders[str(order.id)] = order

    def get_by_id(self, order_id: OrderId) -> Order | None:
        return self._orders.get(str(order_id))
