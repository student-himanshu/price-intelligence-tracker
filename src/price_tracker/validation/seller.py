"""Validation rules for seller data."""

from price_tracker.schemas.seller import SellerCreate


def validate_seller(seller: SellerCreate) -> SellerCreate:
    """Validate and return a seller schema."""
    seller_name = seller.seller_name.strip()

    if not seller_name:
        raise ValueError("Seller name cannot be empty.")

    return seller.model_copy(
        update={"seller_name": seller_name},
    )
    