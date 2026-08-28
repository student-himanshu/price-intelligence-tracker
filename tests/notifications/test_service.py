"""Tests for notification service."""

from decimal import Decimal
from unittest.mock import MagicMock

from price_tracker.notifications.service import NotificationService


def test_notification_is_sent_when_alert_is_triggered() -> None:
    """Notification should be generated at or below target price."""
    alert = MagicMock(
        is_active=True,
        target_price=Decimal("60000.00"),
    )

    product = MagicMock(
        normalized_name="apple iphone 15 128gb",
    )

    result = NotificationService.notify_if_triggered(
        alert=alert,
        product=product,
        current_price=Decimal("59999.00"),
        currency="INR",
    )

    assert result is not None
    assert "apple iphone 15 128gb" in result
    assert "59999.00" in result
    assert "60000.00" in result


def test_notification_is_not_sent_above_target() -> None:
    """Notification should not be generated above target price."""
    alert = MagicMock(
        is_active=True,
        target_price=Decimal("60000.00"),
    )

    product = MagicMock(
        normalized_name="apple iphone 15 128gb",
    )

    result = NotificationService.notify_if_triggered(
        alert=alert,
        product=product,
        current_price=Decimal("61999.00"),
        currency="INR",
    )

    assert result is None


def test_notification_is_not_sent_for_inactive_alert() -> None:
    """Inactive alerts should never generate notifications."""
    alert = MagicMock(
        is_active=False,
        target_price=Decimal("60000.00"),
    )

    product = MagicMock(
        normalized_name="apple iphone 15 128gb",
    )

    result = NotificationService.notify_if_triggered(
        alert=alert,
        product=product,
        current_price=Decimal("59999.00"),
        currency="INR",
    )

    assert result is None


def test_notification_is_not_sent_without_current_price() -> None:
    """Notification should not be generated without price data."""
    alert = MagicMock(
        is_active=True,
        target_price=Decimal("60000.00"),
    )

    product = MagicMock(
        normalized_name="apple iphone 15 128gb",
    )

    result = NotificationService.notify_if_triggered(
        alert=alert,
        product=product,
        current_price=None,
        currency="INR",
    )

    assert result is None