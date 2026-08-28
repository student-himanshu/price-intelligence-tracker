"""Tests for price forecasting."""


from datetime import UTC, datetime
from decimal import Decimal

from price_tracker.analytics.price_forecast import PriceForecastService


def make_history(
    price: str,
    collected_at: datetime,
) -> object:
    """Create a lightweight fake price history record."""
    return type(
        "FakePriceHistory",
        (),
        {
            "price": Decimal(price),
            "collected_at": collected_at,
        },
    )()


def test_forecast_next_price() -> None:
    """Forecast should extend the latest price movement."""
    history = [
        make_history(
            "61999",
            datetime(2026, 8, 27, tzinfo=UTC),
        ),
        make_history(
            "59999",
            datetime(2026, 8, 28, tzinfo=UTC),
        ),
    ]

    result = PriceForecastService.forecast_next_price(history)

    assert result == Decimal("57999")


def test_forecast_next_price_when_price_increases() -> None:
    """Forecast should handle an increasing price."""
    history = [
        make_history(
            "50000",
            datetime(2026, 8, 27, tzinfo=UTC),
        ),
        make_history(
            "52000",
            datetime(2026, 8, 28, tzinfo=UTC),
        ),
    ]

    result = PriceForecastService.forecast_next_price(history)

    assert result == Decimal("54000")


def test_forecast_sorts_history_by_collection_time() -> None:
    """Forecast should use the latest chronological observations."""
    history = [
        make_history(
            "59999",
            datetime(2026, 8, 28, tzinfo=UTC),
        ),
        make_history(
            "61999",
            datetime(2026, 8, 27, tzinfo=UTC),
        ),
    ]

    result = PriceForecastService.forecast_next_price(history)

    assert result == Decimal("57999")


def test_forecast_trend_decreasing() -> None:
    """Trend should be decreasing when the latest price falls."""
    history = [
        make_history(
            "61999",
            datetime(2026, 8, 27, tzinfo=UTC),
        ),
        make_history(
            "59999",
            datetime(2026, 8, 28, tzinfo=UTC),
        ),
    ]

    assert PriceForecastService.trend(history) == "decreasing"


def test_forecast_trend_increasing() -> None:
    """Trend should be increasing when the latest price rises."""
    history = [
        make_history(
            "50000",
            datetime(2026, 8, 27, tzinfo=UTC),
        ),
        make_history(
            "52000",
            datetime(2026, 8, 28, tzinfo=UTC),
        ),
    ]

    assert PriceForecastService.trend(history) == "increasing"


def test_forecast_trend_stable() -> None:
    """Trend should be stable when prices are unchanged."""
    history = [
        make_history(
            "61999",
            datetime(2026, 8, 27, tzinfo=UTC),
        ),
        make_history(
            "61999",
            datetime(2026, 8, 28, tzinfo=UTC),
        ),
    ]

    assert PriceForecastService.trend(history) == "stable"


def test_forecast_trend_insufficient_data() -> None:
    """Trend should require at least two observations."""
    history = [
        make_history(
            "61999",
            datetime(2026, 8, 28, tzinfo=UTC),
        ),
    ]

    assert PriceForecastService.trend(history) == "insufficient_data"


def test_price_change_percentage() -> None:
    """Percentage change should compare the latest two prices."""
    history = [
        make_history(
            "61999",
            datetime(2026, 8, 27, tzinfo=UTC),
        ),
        make_history(
            "59999",
            datetime(2026, 8, 28, tzinfo=UTC),
        ),
    ]

    result = PriceForecastService.price_change_percentage(history)

    assert result == Decimal("-3.2259")


def test_price_change_percentage_requires_two_observations() -> None:
    """Percentage change should require two observations."""
    history = [
        make_history(
            "61999",
            datetime(2026, 8, 28, tzinfo=UTC),
        ),
    ]

    assert PriceForecastService.price_change_percentage(history) is None


def test_price_change_percentage_rejects_zero_previous_price() -> None:
    """Percentage change should return None for a zero base price."""
    history = [
        make_history(
            "0",
            datetime(2026, 8, 27, tzinfo=UTC),
        ),
        make_history(
            "100",
            datetime(2026, 8, 28, tzinfo=UTC),
        ),
    ]

    assert PriceForecastService.price_change_percentage(history) is None


def test_forecast_requires_two_observations() -> None:
    """Forecast should return None with insufficient history."""
    history = [
        make_history(
            "61999",
            datetime(2026, 8, 28, tzinfo=UTC),
        ),
    ]

    result = PriceForecastService.forecast_next_price(history)

    assert result is None


def test_forecast_empty_history() -> None:
    """Forecast should return None for empty history."""
    result = PriceForecastService.forecast_next_price([])

    assert result is None
    
def test_forecast_confidence_is_low_with_insufficient_data() -> None:
    """Confidence should be low with fewer than two observations."""
    history = [
        make_history(
            "61999",
            datetime(2026, 8, 28, tzinfo=UTC),
        ),
    ]

    assert PriceForecastService.confidence(history) == "low"


def test_forecast_confidence_is_medium_with_small_history() -> None:
    """Confidence should be medium with two to four observations."""
    history = [
        make_history(
            "61999",
            datetime(2026, 8, 25, tzinfo=UTC),
        ),
        make_history(
            "60999",
            datetime(2026, 8, 26, tzinfo=UTC),
        ),
        make_history(
            "59999",
            datetime(2026, 8, 27, tzinfo=UTC),
        ),
    ]

    assert PriceForecastService.confidence(history) == "medium"


def test_forecast_confidence_is_high_with_enough_history() -> None:
    """Confidence should be high with at least five observations."""
    history = [
        make_history(
            "61999",
            datetime(2026, 8, 24, tzinfo=UTC),
        ),
        make_history(
            "60999",
            datetime(2026, 8, 25, tzinfo=UTC),
        ),
        make_history(
            "59999",
            datetime(2026, 8, 26, tzinfo=UTC),
        ),
        make_history(
            "58999",
            datetime(2026, 8, 27, tzinfo=UTC),
        ),
        make_history(
            "57999",
            datetime(2026, 8, 28, tzinfo=UTC),
        ),
    ]

    assert PriceForecastService.confidence(history) == "high"