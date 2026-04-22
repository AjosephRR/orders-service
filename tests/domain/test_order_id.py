from uuid import UUID

from orders_service.domain.value_objects.order_id import OrderId


def test_order_id_str_retorna_el_uuid_como_texto() -> None:
    order_id = OrderId(UUID("12345678-1234-5678-1234-567812345678"))

    assert str(order_id) == "12345678-1234-5678-1234-567812345678"
