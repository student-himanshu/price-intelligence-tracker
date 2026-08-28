"""Price forecasting service."""

from decimal import Decimal

from price_tracker.models import PriceHistory


class PriceForecastService:
    """Calculate deterministic price forecasts."""

    @staticmethod
    def forecast_next_price(
        history: list[PriceHistory],
    ) -> Decimal | None:
        """Forecast the next price using the latest price movement."""
        if len(history) < 2:
            return None

        ordered = sorted(
            history,
            key=lambda item: item.collected_at,
        )

        previous_price = ordered[-2].price
        current_price = ordered[-1].price

        change = current_price - previous_price

        return current_price + change

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
    def trend(history: list[PriceHistory]) -> str:
        """Return the current price trend."""
        if len(history) < 2:
            return "insufficient_data"

        ordered = sorted(
            history,
            key=lambda item: item.collected_at,
        )

        previous_price = ordered[-2].price
        current_price = ordered[-1].price

        if current_price > previous_price:
            return "increasing"

        if current_price < previous_price:
            return "decreasing"

        return "stable"

    @staticmethod
    def confidence(history: list[PriceHistory]) -> str:
        """Return a simple confidence level based on history length."""
        count = len(history)

        if count < 2:
            return "low"

        if count < 5:
            return "medium"

        return "high"