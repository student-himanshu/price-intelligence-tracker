"""Tests for forecast explanations."""
from decimal import Decimal

from price_tracker.analytics.forecast_explanation import (
    ForecastExplanationService,
)


def test_explanation_for_decreasing_trend() -> None:
    """Explanation should describe a decreasing price trend."""
    result = ForecastExplanationService.explain(
        current_price=Decimal("59999.00"),
        forecast_price=Decimal("57999.00"),
        price_change=Decimal("-2000.00"),
        trend="decreasing",
        currency="INR",
    )
    assert result == (
        "The current price is INR 59999.00 "
        "and the forecast price is INR 57999.00. "
        "The recent price trend is decreasing."
    )
def test_explanation_for_increasing_trend() -> None:
    """Explanation should describe an increasing price trend."""
    result = ForecastExplanationService.explain(
        current_price=Decimal("52000.00"),
        forecast_price=Decimal("54000.00"),
        price_change=Decimal("2000.00"),
        trend="increasing",
        currency="INR",
    )
    assert result == (
        "The current price is INR 52000.00 "
        "and the forecast price is INR 54000.00. "
        "The recent price trend is increasing."
    )
def test_explanation_for_stable_trend() -> None:
    """Explanation should describe a stable price trend."""
    result = ForecastExplanationService.explain(
        current_price=Decimal("61999.00"),
        forecast_price=Decimal("61999.00"),
        price_change=Decimal("0.00"),
        trend="stable",
        currency="INR",
    )
    assert result == (
        "The current price is INR 61999.00 "
        "and the forecast price is INR 61999.00. "
        "The recent price trend is stable."
    )
def test_explanation_with_insufficient_history() -> None:
    """Explanation should handle missing forecast data."""
    result = ForecastExplanationService.explain(
        current_price=None,
        forecast_price=None,
        price_change=None,
        trend="insufficient_data",
        currency="INR",
    )
    assert result == (
        "There is not enough price history to generate a forecast."
    )
def test_explanation_with_only_current_price() -> None:
    """Explanation should request more observations when needed."""
    result = ForecastExplanationService.explain(
        current_price=Decimal("61999.00"),
        forecast_price=None,
        price_change=None,
        trend="insufficient_data",
        currency="INR",
    )
    assert result == (
        "There is not enough price history to generate "
        "a reliable forecast."
    )
