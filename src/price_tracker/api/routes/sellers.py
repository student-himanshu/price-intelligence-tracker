"""Seller API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from price_tracker.api.dependencies import get_db
from price_tracker.schemas.seller import SellerRead
from price_tracker.services.seller_service import SellerService

router = APIRouter(prefix="/sellers", tags=["Sellers"])


@router.get("/{seller_id}", response_model=SellerRead)
def get_seller(
    seller_id: int,
    db: Session = Depends(get_db),
) -> SellerRead:
    """Return a seller by ID."""
    service = SellerService(db)
    seller = service.get_by_id(seller_id)

    if seller is None:
        raise HTTPException(
            status_code=404,
            detail="Seller not found.",
        )

    return SellerRead.model_validate(seller)