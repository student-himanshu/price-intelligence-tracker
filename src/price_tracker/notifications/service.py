"""Price alert notification service."""

from decimal import Decimal

from price_tracker.models import PriceAlert, Product
from price_tracker.notifications.console import ConsoleNotification


class NotificationService:
    """Evaluate and send price-alert notifications."""

    @staticmethod
    def notify_if_triggered(
        alert: PriceAlert,
        product: Product,
        current_price: Decimal | None,
        currency: str,
    ) -> str | None:
        """Send a notification when an active alert is triggered."""
        if not alert.is_active:
            return None

        if current_price is None:
            return None

        if current_price > alert.target_price:
            return None

        return ConsoleNotification.send(
            alert=alert,
            product=product,
            current_price=current_price,
            currency=currency,
        )