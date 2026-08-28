"""Price analytics API endpoints."""

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from price_tracker.analytics.price_analytics import PriceAnalyticsService
from price_tracker.database.session import get_session
from price_tracker.models import Listing, PriceHistory, Product, Seller
from price_tracker.services.price_history_service import PriceHistoryService

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)


@router.get("/listings/{listing_id}")
def get_listing_analytics(
    listing_id: int,
    session: Session = Depends(get_session),
) -> dict[str, Decimal | None]:
    """Return price analytics for a listing."""
    history_service = PriceHistoryService(session)
    history = history_service.get_by_listing_id(listing_id)

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Price history not found.",
        )

    analytics = PriceAnalyticsService()
    latest = history[-1]

    return {
        "current_price": analytics.current_price(history),
        "lowest_price": analytics.lowest_price(history),
        "highest_price": analytics.highest_price(history),
        "average_price": analytics.average_price(history),
        "price_change": analytics.price_change(history),
        "price_change_percentage": analytics.price_change_percentage(history),
        "discount_percentage": analytics.discount_percentage(
            latest.price,
            latest.original_price,
        ),
    }


@router.get("/products/{product_id}/history")
def get_product_price_history(
    product_id: int,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    """Return price history for all listings of a product."""
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

    history: list[dict[str, object]] = []

    for listing in listings:
        seller = session.get(Seller, listing.seller_id)

        if seller is None:
            continue

        records = (
            session.query(PriceHistory)
            .filter(PriceHistory.listing_id == listing.id)
            .order_by(PriceHistory.collected_at.asc())
            .all()
        )

        for record in records:
            history.append(
                {
                    "listing_id": listing.id,
                    "seller_id": seller.id,
                    "seller_name": seller.seller_name,
                    "price": record.price,
                    "currency": record.currency,
                    "collected_at": record.collected_at,
                }
            )

    history.sort(key=lambda item: item["collected_at"])

    return {
        "product_id": product.id,
        "product_name": product.normalized_name,
        "observation_count": len(history),
        "history": history,
    }