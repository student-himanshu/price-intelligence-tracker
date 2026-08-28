"""Persistent price alert API endpoints."""
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from price_tracker.database.session import get_session
from price_tracker.models import PriceAlert, Product

router = APIRouter(
    prefix="/price-alerts",
    tags=["Price Alerts"],
)
@router.post("/{product_id}")
def create_price_alert(
    product_id: int,
    target_price: Decimal,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    """Create a price alert for a product."""
    product = session.get(Product, product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found.",
        )
    alert = PriceAlert(
        product_id=product_id,
        target_price=target_price,
    )
    session.add(alert)
    session.commit()
    session.refresh(alert)
    return {
        "id": alert.id,
        "product_id": alert.product_id,
        "target_price": alert.target_price,
        "is_active": alert.is_active,
        "created_at": alert.created_at,
        "triggered_at": alert.triggered_at,
    }
@router.get("/{product_id}")
def list_price_alerts(
    product_id: int,
    session: Session = Depends(get_session),
) -> list[dict[str, object]]:
    """Return all price alerts for a product."""
    product = session.get(Product, product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found.",
        )
    alerts = (
        session.query(PriceAlert)
        .filter(PriceAlert.product_id == product_id)
        .order_by(PriceAlert.created_at.desc())
        .all()
    )
    return [
        {
            "id": alert.id,
            "product_id": alert.product_id,
            "target_price": alert.target_price,
            "is_active": alert.is_active,
            "created_at": alert.created_at,
            "triggered_at": alert.triggered_at,
        }
        for alert in alerts
    ]
@router.delete("/{alert_id}")
def deactivate_price_alert(
    alert_id: int,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    """Deactivate an existing price alert."""
    alert = session.get(PriceAlert, alert_id)
    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Price alert not found.",
        )
    alert.is_active = False
    session.commit()
    session.refresh(alert)
    return {
        "id": alert.id,
        "product_id": alert.product_id,
        "target_price": alert.target_price,
        "is_active": alert.is_active,
        "triggered_at": alert.triggered_at,
    }
