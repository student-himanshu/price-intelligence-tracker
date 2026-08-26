"""Product validation schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    """Shared product fields."""

    brand: str | None = Field(default=None, max_length=100)
    model: str | None = Field(default=None, max_length=150)
    normalized_name: str = Field(min_length=1, max_length=255)
    category: str | None = Field(default=None, max_length=100)


class ProductCreate(ProductBase):
    """Schema for creating a product."""

    pass


class ProductRead(ProductBase):
    """Schema for returning a product."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime