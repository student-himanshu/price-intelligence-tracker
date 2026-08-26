"""Validation rules for price history data."""

from decimal import Decimal

from price_tracker.schemas.price_history import PriceHistoryCreate


def validate_price_history(
    price_history: PriceHistoryCreate,
) -> PriceHistoryCreate:
    """Validate price history values."""
    if price_history.price <= Decimal("0"):
        raise ValueError("Price must be greater than zero.")

    if (
        price_history.original_price is not None
        and price_history.original_price < price_history.price
    ):
        raise ValueError(
            "Original price cannot be lower than the current price.",
        )

    return price_history