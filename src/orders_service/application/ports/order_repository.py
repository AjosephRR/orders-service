from abc import ABC, abstractmethod

from orders_service.domain.entities.order import Order
from orders_service.domain.value_objects.order_id import OrderId


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> None:
        pass

    @abstractmethod
    def get_by_id(self, order_id: OrderId) -> Order | None:
        pass
