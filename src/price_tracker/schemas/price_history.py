"""Price history validation schemas."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PriceHistoryBase(BaseModel):
    """Shared price history fields."""

    listing_id: int = Field(gt=0)
    price: Decimal = Field(gt=0, decimal_places=2, max_digits=12)
    original_price: Decimal | None = Field(
        default=None,
        gt=0,
        decimal_places=2,
        max_digits=12,
    )
    discount_percentage: Decimal | None = Field(
        default=None,
        ge=0,
        le=100,
        decimal_places=2,
        max_digits=5,
    )
    currency: str = Field(default="INR", min_length=3, max_length=3)


class PriceHistoryCreate(PriceHistoryBase):
    """Schema for creating a price history record."""

    pass


class PriceHistoryRead(PriceHistoryBase):
    """Schema for returning a price history record."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    collected_at: datetime