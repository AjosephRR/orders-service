from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True)
class OrderId:
    value: UUID

    @staticmethod
    def new() -> "OrderId":
        return OrderId(uuid4())

    @staticmethod
    def from_string(value: str) -> "OrderId":
        return OrderId(UUID(value))

    def __str__(self) -> str:
        return str(self.value)
