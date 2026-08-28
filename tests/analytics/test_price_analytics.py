"""Tests for price analytics."""
from datetime import UTC, datetime
from decimal import Decimal

from price_tracker.analytics.price_analytics import PriceAnalyticsService


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
def test_current_price_returns_latest_price() -> None:
    """Current price should come from the latest observation."""
    history = [
        make_history(
            "61999",
            datetime(2026, 8, 27, 10, 0, tzinfo=UTC),
        ),
        make_history(
            "59999",
            datetime(2026, 8, 28, 10, 0, tzinfo=UTC),
        ),
    ]
    assert PriceAnalyticsService.current_price(history) == Decimal("59999")
def test_lowest_price() -> None:
    """Lowest price should be returned."""
    history = [
        make_history("61999", datetime(2026, 8, 27, tzinfo=UTC)),
        make_history("59999", datetime(2026, 8, 28, tzinfo=UTC)),
        make_history("62999", datetime(2026, 8, 29, tzinfo=UTC)),
    ]
    assert PriceAnalyticsService.lowest_price(history) == Decimal("59999")
def test_highest_price() -> None:
    """Highest price should be returned."""
    history = [
        make_history("61999", datetime(2026, 8, 27, tzinfo=UTC)),
        make_history("59999", datetime(2026, 8, 28, tzinfo=UTC)),
        make_history("62999", datetime(2026, 8, 29, tzinfo=UTC)),
    ]
    assert PriceAnalyticsService.highest_price(history) == Decimal("62999")
def test_average_price() -> None:
    """Average price should be calculated correctly."""
    history = [
        make_history("60000", datetime(2026, 8, 27, tzinfo=UTC)),
        make_history("62000", datetime(2026, 8, 28, tzinfo=UTC)),
    ]
    assert PriceAnalyticsService.average_price(history) == Decimal("61000")
def test_price_change() -> None:
    """Price change should compare the latest two observations."""
    history = [
        make_history("61999", datetime(2026, 8, 27, tzinfo=UTC)),
        make_history("59999", datetime(2026, 8, 28, tzinfo=UTC)),
    ]
    assert PriceAnalyticsService.price_change(history) == Decimal("-2000")
    

def test_discount_percentage() -> None:
    """Discount percentage should be calculated correctly."""
    result = PriceAnalyticsService.discount_percentage(
        Decimal("800"),
        Decimal("1000"),
    )
    assert result == Decimal("20")
def test_discount_percentage_when_no_original_price() -> None:
    """Missing original price should produce no discount."""
    result = PriceAnalyticsService.discount_percentage(
        Decimal("800"),
        None,
    )
    assert result is None
def test_empty_history_returns_none() -> None:
    """Analytics should safely handle empty history."""
    service = PriceAnalyticsService()
    assert service.current_price([]) is None
    assert service.lowest_price([]) is None
    assert service.highest_price([]) is None
    assert service.average_price([]) is None
    assert service.price_change([]) is None
def test_price_change_requires_two_observations() -> None:
    """Price change requires at least two observations."""
    history = [
        make_history(
            "61999",
            datetime(2026, 8, 27, tzinfo=UTC),
        ),
    ]
    assert PriceAnalyticsService.price_change(history) is None

def test_price_change_percentage() -> None:
    """Price change percentage should compare the latest two prices."""
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

    result = PriceAnalyticsService.price_change_percentage(history)

    assert result == Decimal("-3.2259")