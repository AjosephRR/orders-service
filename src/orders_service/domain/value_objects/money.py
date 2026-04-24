from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal, getcontext

from orders_service.domain.exceptions.domain_exceptions import (
    InvalidOrderTotalError,
)

# Configuración opcional de precisión global (puede ajustarse si se necesita)
getcontext().prec = 28  # precisión estándar alta


@dataclass(frozen=True)
class Money:
    amount: Decimal

    def __post_init__(self) -> None:
        # Convertir a Decimal si viene como int/str
        value = Decimal(self.amount)

        # Normalizar a 2 decimales con redondeo financiero estándar
        normalized = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        if normalized < Decimal("0.00"):
            raise InvalidOrderTotalError("El total no puede ser negativo.")

        # Como es frozen=True, usamos object.__setattr__
        object.__setattr__(self, "amount", normalized)
