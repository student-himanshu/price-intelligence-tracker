"""Repository operations for listings."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from price_tracker.models.listing import Listing


class ListingRepository:
    """Provide database operations for Listing entities."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, listing_id: int) -> Listing | None:
        """Return a listing by its primary key."""
        return self.session.get(Listing, listing_id)

    def get_by_external_product_id(
        self,
        seller_id: int,
        external_product_id: str,
    ) -> Listing | None:
        """Return a seller listing by its external product ID."""
        statement = select(Listing).where(
            Listing.seller_id == seller_id,
            Listing.external_product_id == external_product_id,
        )
        return self.session.scalar(statement)

    def list_by_product(self, product_id: int) -> list[Listing]:
        """Return all listings for a product."""
        statement = (
            select(Listing)
            .where(Listing.product_id == product_id)
            .order_by(Listing.id)
        )
        return list(self.session.scalars(statement).all())

    def list_available_by_product(self, product_id: int) -> list[Listing]:
        """Return available listings for a product."""
        statement = (
            select(Listing)
            .where(
                Listing.product_id == product_id,
                Listing.availability.is_(True),
            )
            .order_by(Listing.id)
        )
        return list(self.session.scalars(statement).all())

    def add(self, listing: Listing) -> Listing:
        """Add a listing to the current transaction."""
        self.session.add(listing)
        self.session.flush()
        return listing