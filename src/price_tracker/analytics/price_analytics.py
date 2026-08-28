"""Price analytics service."""

from decimal import Decimal

from price_tracker.models import PriceHistory


class PriceAnalyticsService:
    """Calculate price intelligence from price history records."""

    @staticmethod
    def current_price(history: list[PriceHistory]) -> Decimal | None:
        """Return the most recent recorded price."""
        if not history:
            return None

        latest = max(
            history,
            key=lambda item: item.collected_at,
        )

        return latest.price

    @staticmethod
    def lowest_price(history: list[PriceHistory]) -> Decimal | None:
        """Return the lowest recorded price."""
        if not history:
            return None

        return min(item.price for item in history)

    @staticmethod
    def highest_price(history: list[PriceHistory]) -> Decimal | None:
        """Return the highest recorded price."""
        if not history:
            return None

        return max(item.price for item in history)

    @staticmethod
    def average_price(history: list[PriceHistory]) -> Decimal | None:
        """Return the average recorded price."""
        if not history:
            return None

        total = sum(
            (item.price for item in history),
            Decimal("0"),
        )

        return total / len(history)

    @staticmethod
    def price_change(
        history: list[PriceHistory],
    ) -> Decimal | None:
        """Return current price minus the previous recorded price."""
        if len(history) < 2:
            return None

        ordered = sorted(
            history,
            key=lambda item: item.collected_at,
        )

        return ordered[-1].price - ordered[-2].price

    @staticmethod
    def price_change_percentage(
        history: list[PriceHistory],
    ) -> Decimal | None:
        """Return percentage change between the latest two prices."""
        if len(history) < 2:
            return None

        ordered = sorted(
            history,
            key=lambda item: item.collected_at,
        )

        previous_price = ordered[-2].price

        if previous_price <= 0:
            return None

        current_price = ordered[-1].price

        return (
            (current_price - previous_price)
            / previous_price
            * Decimal("100")
        ).quantize(Decimal("0.0001"))
        
        
    @staticmethod
    def discount_percentage(
        price: Decimal,
        original_price: Decimal | None,
    ) -> Decimal | None:
        """Calculate discount percentage from original and current price."""
        if original_price is None or original_price <= 0:
            return None

        if price >= original_price:
            return Decimal("0")

        return ((original_price - price) / original_price) * Decimal("100")