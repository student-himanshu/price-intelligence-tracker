"""Price history API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from price_tracker.api.dependencies import get_db
from price_tracker.services.price_history_service import PriceHistoryService

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get("/{price_history_id}")
def get_price_history(
    price_history_id: int,
    db: Session = Depends(get_db),
) -> dict[str, object]:
    """Return a price history record by ID."""
    service = PriceHistoryService(db)
    price_history = service.get_by_id(price_history_id)

    if price_history is None:
        raise HTTPException(
            status_code=404,
            detail="Price history record not found.",
        )

    return {
        "id": price_history.id,
        "listing_id": price_history.listing_id,
        "price": price_history.price,
        "original_price": price_history.original_price,
        "currency": price_history.currency,
        "recorded_at": price_history.recorded_at,
    }