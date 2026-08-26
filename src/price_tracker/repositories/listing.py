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

    def get_by_external_product_id(
        self,
        seller_id: int,
        external_product_id: str,
    ) -> Listing | None:
        """Return a listing by seller and external product ID."""
        statement = select(Listing).where(
            Listing.seller_id == seller_id,
            Listing.external_product_id == external_product_id,
        )

        return self.session.scalar(statement)

    def add(self, listing: Listing) -> Listing:
        """Add a listing and flush it to the database session."""
        self.session.add(listing)
        self.session.flush()

        return listing

    def list_by_product(self, product_id: int) -> list[Listing]:
        """Return all listings for a product."""
        statement = select(Listing).where(
            Listing.product_id == product_id,
        )

        return list(self.session.scalars(statement).all())