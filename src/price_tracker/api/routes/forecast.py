"""Price forecasting API routes."""

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from price_tracker.analytics.forecast_explanation import (
    ForecastExplanationService,
)
from price_tracker.analytics.price_forecast import PriceForecastService
from price_tracker.database.session import get_session
from price_tracker.models import Listing, PriceHistory, Product

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"],
)


@router.get("/{product_id}")
def forecast_product_price(
    product_id: int,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    """Return a price forecast and explanation for a product."""
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

    all_history.sort(
        key=lambda item: item.collected_at,
    )

    forecast = PriceForecastService.forecast_next_price(
        all_history,
    )

    current_price: Decimal | None = (
        all_history[-1].price
        if all_history
        else None
    )

    price_change: Decimal | None = None

    if len(all_history) >= 2:
        price_change = (
            all_history[-1].price
            - all_history[-2].price
        )

    price_change_percentage = (
        PriceForecastService.price_change_percentage(
            all_history,
        )
    )

    trend = PriceForecastService.trend(all_history)
    confidence = PriceForecastService.confidence(all_history)

    currency = (
        all_history[-1].currency
        if all_history
        else "INR"
    )

    explanation = ForecastExplanationService.explain(
        current_price=current_price,
        forecast_price=forecast,
        price_change=price_change,
        trend=trend,
        currency=currency,
    )

    return {
        "product_id": product.id,
        "product_name": product.normalized_name,
        "current_price": current_price,
        "forecast_price": forecast,
        "price_change": price_change,
        "price_change_percentage": price_change_percentage,
        "trend": trend,
        "confidence": confidence,
        "currency": currency,
        "history_count": len(all_history),
        "explanation": explanation,
    }