"""Listing validation schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ListingBase(BaseModel):
    """Shared listing fields."""

    product_id: int = Field(gt=0)
    seller_id: int = Field(gt=0)
    url: str = Field(min_length=1, max_length=1000)
    external_product_id: str | None = Field(default=None, max_length=255)
    availability: bool = True


class ListingCreate(ListingBase):
    """Schema for creating a listing."""

    pass


class ListingRead(ListingBase):
    """Schema for returning a listing."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime