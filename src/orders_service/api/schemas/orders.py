from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class OrderCreateRequest(BaseModel):
    total: Decimal = Field(gt=0)
    customer_name: str | None = Field(default=None, min_length=1, max_length=100)
    customer_email: str | None = Field(default=None, min_length=3, max_length=255)
    shipping_address: str | None = Field(default=None, min_length=5, max_length=255)
    notes: str | None = Field(default=None, min_length=1, max_length=500)


class OrderResponse(BaseModel):
    id: str
    total: Decimal
    customer_name: str | None
    customer_email: str | None
    shipping_address: str | None
    notes: str | None
    status: str
    created_at: datetime
