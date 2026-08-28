"""Console notification provider."""

from price_tracker.models import PriceAlert, Product


class ConsoleNotification:
    """Send price-alert notifications to the console."""

    @staticmethod
    def send(
        alert: PriceAlert,
        product: Product,
        current_price: object,
        currency: str,
    ) -> str:
        """Return a formatted price-alert notification."""
        message = (
            f"PRICE ALERT: {product.normalized_name} "
            f"is now {currency} {current_price}. "
            f"Target price: {currency} {alert.target_price}."
        )

        print(message)

        return message