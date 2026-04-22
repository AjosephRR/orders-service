from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class OrderCreateRequest(BaseModel):
    total: Decimal = Field(gt=0)


class OrderResponse(BaseModel):
    id: str
    total: Decimal
    status: str
    created_at: datetime
