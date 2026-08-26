"""Validation rules for product data."""

from price_tracker.schemas.product import ProductCreate


def validate_product(product: ProductCreate) -> ProductCreate:
    """Validate and return a product schema."""
    normalized_name = product.normalized_name.strip()

    if not normalized_name:
        raise ValueError("Product normalized_name cannot be empty.")

    return product.model_copy(
        update={"normalized_name": normalized_name},
    )