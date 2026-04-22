class ApplicationError(Exception):
    """Base exception for application layer."""


class OrderNotFoundError(ApplicationError):
    """Raised when an order is not found."""
