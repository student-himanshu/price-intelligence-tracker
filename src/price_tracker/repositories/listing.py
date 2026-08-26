"""Listing repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from price_tracker.models import Listing


class ListingRepository:
    """Data-access operations for listings."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, listing_id: int) -> Listing | None:
        """Return a listing by ID."""
        statement = select(Listing).where(Listing.id == listing_id)

        return self.session.scalar(statement)