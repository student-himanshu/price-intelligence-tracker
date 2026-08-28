"""Generate human-readable explanations for price forecasts."""

from decimal import Decimal


class ForecastExplanationService:
    """Create deterministic explanations for price forecasts."""

    @staticmethod
    def explain(
        current_price: Decimal | None,
        forecast_price: Decimal | None,
        price_change: Decimal | None,
        trend: str,
        currency: str,
    ) -> str:
        """Return a concise explanation of the forecast."""
        if current_price is None:
            return "There is not enough price history to generate a forecast."

        if forecast_price is None:
            return (
                "There is not enough price history to generate "
                "a reliable forecast."
            )

        if price_change is None:
            return (
                f"The current price is {currency} {current_price:.2f}. "
                "More price observations are needed to determine the trend."
            )

        if trend == "increasing":
            return (
                f"The current price is {currency} {current_price:.2f} "
                f"and the forecast price is {currency} {forecast_price:.2f}. "
                "The recent price trend is increasing."
            )

        if trend == "decreasing":
            return (
                f"The current price is {currency} {current_price:.2f} "
                f"and the forecast price is {currency} {forecast_price:.2f}. "
                "The recent price trend is decreasing."
            )

        return (
            f"The current price is {currency} {current_price:.2f} "
            f"and the forecast price is {currency} {forecast_price:.2f}. "
            "The recent price trend is stable."
        )
        