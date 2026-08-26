"""Application services for listings."""

from sqlalchemy.orm import Session

from price_tracker.models.listing import Listing
from price_tracker.repositories.listing import ListingRepository
from price_tracker.schemas.listing import ListingCreate
from price_tracker.validation.listing import validate_listing


class ListingService:
    """Handle listing business operations."""

    def __init__(self, session: Session) -> None:
        self.repository = ListingRepository(session)

    def get_by_id(self, listing_id: int) -> Listing | None:
        """Return a listing by ID."""
        return self.repository.get_by_id(listing_id)

    def get_or_create(self, listing: ListingCreate) -> Listing:
        """Return an existing listing or create a new one."""
        validated_listing = validate_listing(listing)

        if validated_listing.external_product_id is not None:
            existing = self.repository.get_by_external_product_id(
                validated_listing.seller_id,
                validated_listing.external_product_id,
            )

            if existing is not None:
                return existing

        new_listing = Listing(**validated_listing.model_dump())
        return self.repository.add(new_listing)

    def list_by_product(self, product_id: int) -> list[Listing]:
        """Return all listings for a product."""
        return self.repository.list_by_product(product_id)