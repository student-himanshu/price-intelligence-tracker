"""Tests for price alert analytics."""
from datetime import UTC, datetime
from decimal import Decimal

from price_tracker.analytics.price_alert import PriceAlertService


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
            "currency": "INR",
        },
    )()
def test_is_triggered_when_price_reaches_target() -> None:
    """Alert should trigger at or below the target price."""
    assert PriceAlertService.is_triggered(
        Decimal("59999"),
        Decimal("60000"),
    )
def test_is_not_triggered_when_price_is_above_target() -> None:
    """Alert should not trigger above the target price."""
    assert not PriceAlertService.is_triggered(
        Decimal("61999"),
        Decimal("60000"),
    )
def test_is_not_triggered_without_current_price() -> None:
    """Alert should not trigger without price data."""
    assert not PriceAlertService.is_triggered(
        None,
        Decimal("60000"),
    )
def test_price_difference() -> None:
    """Price difference should be target minus current price."""
    assert PriceAlertService.price_difference(
        Decimal("59999"),
        Decimal("60000"),
    ) == Decimal("1")
def test_price_difference_when_price_is_above_target() -> None:
    """Difference should be negative when current price is above target."""
    assert PriceAlertService.price_difference(
        Decimal("61999"),
        Decimal("60000"),
    ) == Decimal("-1999")
def test_price_difference_without_current_price() -> None:
    """Difference should be None without price data."""
    assert PriceAlertService.price_difference(
        None,
        Decimal("60000"),
    ) is None
def test_latest_price_returns_most_recent_observation() -> None:
    """Latest price should be selected chronologically."""
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
    latest = PriceAlertService.latest_price(history)
    assert latest is not None
    assert latest.price == Decimal("59999")
def test_latest_price_with_empty_history() -> None:
    """Latest price should be None for empty history."""
    assert PriceAlertService.latest_price([]) is None
