"""Seller validation schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SellerBase(BaseModel):
    """Shared seller fields."""

    seller_name: str = Field(min_length=1, max_length=150)
    domain: str | None = Field(default=None, max_length=255)


class SellerCreate(SellerBase):
    """Schema for creating a seller."""

    pass


class SellerRead(SellerBase):
    """Schema for returning a seller."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime