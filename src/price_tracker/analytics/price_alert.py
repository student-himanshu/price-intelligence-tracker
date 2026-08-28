"""Price alert analytics service."""
from decimal import Decimal

from price_tracker.models import PriceHistory


class PriceAlertService:
    """Evaluate product prices against target prices."""
    @staticmethod
    def is_triggered(
        current_price: Decimal | None,
        target_price: Decimal,
    ) -> bool:
        """Return whether the current price has reached the target."""
        if current_price is None:
            return False
        return current_price <= target_price
    @staticmethod
    def price_difference(
        current_price: Decimal | None,
        target_price: Decimal,
    ) -> Decimal | None:
        """Return the difference between target and current price."""
        if current_price is None:
            return None
        return target_price - current_price
    @staticmethod
    def latest_price(
        history: list[PriceHistory],
    ) -> PriceHistory | None:
        """Return the most recent price observation."""
        if not history:
            return None
        return max(
            history,
            key=lambda item: item.collected_at,
        )
