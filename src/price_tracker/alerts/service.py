"""Persistent price alert evaluation service."""
from decimal import Decimal

from sqlalchemy.orm import Session

from price_tracker.models import PriceAlert, Product


class AlertService:
    """Evaluate persistent price alerts."""
    @staticmethod
    def get_active_alerts(
        session: Session,
        product_id: int,
    ) -> list[PriceAlert]:
        """Return active alerts for a product."""
        return (
            session.query(PriceAlert)
            .filter(
                PriceAlert.product_id == product_id,
                PriceAlert.is_active.is_(True),
            )
            .order_by(PriceAlert.created_at.asc())
            .all()
        )
    @staticmethod
    def should_trigger(
        current_price: Decimal | None,
        target_price: Decimal,
    ) -> bool:
        """Return whether the current price reaches the target."""
        if current_price is None:
            return False
        return current_price <= target_price
    @staticmethod
    def evaluate(
        session: Session,
        product: Product,
        current_price: Decimal | None,
    ) -> list[PriceAlert]:
        """Return active alerts triggered by the current price."""
        alerts = AlertService.get_active_alerts(
            session,
            product.id,
        )
        return [
            alert
            for alert in alerts
            if AlertService.should_trigger(
                current_price,
                alert.target_price,
            )
        ]
