"""Price history API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from price_tracker.api.dependencies import get_db
from price_tracker.schemas.price_history import PriceHistoryRead
from price_tracker.services.price_history_service import PriceHistoryService

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get("/{price_history_id}", response_model=PriceHistoryRead)
def get_price_history(
    price_history_id: int,
    db: Session = Depends(get_db),
) -> PriceHistoryRead:
    """Return a price history record by ID."""
    service = PriceHistoryService(db)
    price_history = service.get_by_id(price_history_id)

    if price_history is None:
        raise HTTPException(
            status_code=404,
            detail="Price history record not found.",
        )

    return PriceHistoryRead.model_validate(price_history)