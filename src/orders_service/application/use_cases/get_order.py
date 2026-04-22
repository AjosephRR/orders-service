from orders_service.application.ports.order_repository import OrderRepository
from orders_service.application.exceptions import OrderNotFoundError
from orders_service.domain.entities.order import Order
from orders_service.domain.value_objects.order_id import OrderId


class GetOrder:

    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    def execute(self, order_id: OrderId) -> Order:
        order = self._repository.get_by_id(order_id)

        if order is None:
            raise OrderNotFoundError(
                f"Order with id {order_id} not found."
            )

        return order
