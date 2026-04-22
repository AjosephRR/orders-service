class DomainError(Exception):
    """Excepción base para errores del dominio."""


class InvalidOrderTotalError(DomainError):
    """Se lanza cuando el total de la orden es inválido."""


class InvalidOrderStateTransitionError(DomainError):
    """Se lanza cuando se intenta una transición de estado inválida."""
