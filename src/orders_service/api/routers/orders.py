from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from orders_service.api.schemas.orders import (
    OrderCreateRequest,
    OrderResponse,
)
from orders_service.application.use_cases.create_order import CreateOrder
from orders_service.application.use_cases.get_order import GetOrder
from orders_service.application.exceptions import OrderNotFoundError
from orders_service.domain.value_objects.order_id import OrderId
from orders_service.api.dependencies import get_repository


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse)
def create_order(
    request: OrderCreateRequest,
    repository=Depends(get_repository),
):
    use_case = CreateOrder(repository)
    order = use_case.execute(request.total)

    return OrderResponse(
        id=str(order.id),
        total=order.total.amount,
        status=order.status.value,
        created_at=order.created_at,
    )


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: UUID, repository=Depends(get_repository)):
    use_case = GetOrder(repository)

    try:
        order = use_case.execute(OrderId(order_id))
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")

    return OrderResponse(
        id=str(order.id),
        total=order.total.amount,
        status=order.status.value,
        created_at=order.created_at,
    )
