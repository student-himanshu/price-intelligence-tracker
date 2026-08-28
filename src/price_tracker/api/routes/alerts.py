"""Price alert API endpoints."""
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from price_tracker.analytics.price_alert import PriceAlertService
from price_tracker.database.session import get_session
from price_tracker.models import Listing, PriceHistory, Product

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)
@router.get("/{product_id}")
def check_price_alert(
    product_id: int,
    target_price: Decimal,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    """Check whether the latest product price meets a target price."""
    product = session.get(Product, product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found.",
        )
    listings = (
        session.query(Listing)
        .filter(Listing.product_id == product_id)
        .all()
    )
    all_history: list[PriceHistory] = []
    for listing in listings:
        history = (
            session.query(PriceHistory)
            .filter(PriceHistory.listing_id == listing.id)
            .order_by(PriceHistory.collected_at.asc())
            .all()
        )
        all_history.extend(history)
    latest = PriceAlertService.latest_price(all_history)
    current_price = (
        latest.price
        if latest is not None
        else None
    )
    return {
        "product_id": product.id,
        "product_name": product.normalized_name,
        "current_price": current_price,
        "target_price": target_price,
        "price_difference": PriceAlertService.price_difference(
            current_price,
            target_price,
        ),
        "triggered": PriceAlertService.is_triggered(
            current_price,
            target_price,
        ),
        "currency": (
            latest.currency
            if latest is not None
            else "INR"
        ),
    }
