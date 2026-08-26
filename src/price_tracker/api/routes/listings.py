"""Listing API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from price_tracker.api.dependencies import get_db
from price_tracker.services.listing_service import ListingService

router = APIRouter(prefix="/listings", tags=["Listings"])


@router.get("/{listing_id}")
def get_listing(
    listing_id: int,
    db: Session = Depends(get_db),
) -> dict[str, object]:
    """Return a listing by ID."""
    service = ListingService(db)
    listing = service.get_by_id(listing_id)

    if listing is None:
        raise HTTPException(
            status_code=404,
            detail="Listing not found.",
        )

    return {
        "id": listing.id,
        "product_id": listing.product_id,
        "seller_id": listing.seller_id,
        "url": listing.url,
        "external_product_id": listing.external_product_id,
        "availability": listing.availability,
    }