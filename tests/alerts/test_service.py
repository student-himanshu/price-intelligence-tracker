"""Tests for persistent price alert evaluation."""
from decimal import Decimal
from unittest.mock import MagicMock

from price_tracker.alerts.service import AlertService


def test_should_trigger_when_price_reaches_target() -> None:
    """Alert should trigger when price equals target."""
    assert AlertService.should_trigger(
        Decimal("50000.00"),
        Decimal("50000.00"),
    )
def test_should_trigger_when_price_is_below_target() -> None:
    """Alert should trigger when price is below target."""
    assert AlertService.should_trigger(
        Decimal("49000.00"),
        Decimal("50000.00"),
    )
def test_should_not_trigger_when_price_is_above_target() -> None:
    """Alert should not trigger when price is above target."""
    assert not AlertService.should_trigger(
        Decimal("51000.00"),
        Decimal("50000.00"),
    )
def test_should_not_trigger_without_current_price() -> None:
    """Alert should not trigger without a current price."""
    assert not AlertService.should_trigger(
        None,
        Decimal("50000.00"),
    )
def test_evaluate_returns_only_triggered_active_alerts() -> None:
    """Evaluation should return only alerts that reach their target."""
    product = MagicMock(id=262)
    triggered_alert = MagicMock(
        product_id=262,
        is_active=True,
        target_price=Decimal("62000.00"),
    )
    non_triggered_alert = MagicMock(
        product_id=262,
        is_active=True,
        target_price=Decimal("60000.00"),
    )
    session = MagicMock()
    query = session.query.return_value
    query.filter.return_value.order_by.return_value.all.return_value = [
        triggered_alert,
        non_triggered_alert,
    ]
    result = AlertService.evaluate(
        session,
        product,
        Decimal("61999.00"),
    )
    assert result == [triggered_alert]
