"""Application services for sellers."""

from sqlalchemy.orm import Session

from price_tracker.models.seller import Seller
from price_tracker.repositories.seller import SellerRepository
from price_tracker.schemas.seller import SellerCreate
from price_tracker.validation.seller import validate_seller


class SellerService:
    """Handle seller business operations."""

    def __init__(self, session: Session) -> None:
        self.repository = SellerRepository(session)

    def get_by_id(self, seller_id: int) -> Seller | None:
        """Return a seller by ID."""
        return self.repository.get_by_id(seller_id)

    def get_or_create(self, seller: SellerCreate) -> Seller:
        """Return an existing seller or create a new one."""
        validated_seller = validate_seller(seller)

        existing = self.repository.get_by_name(
            validated_seller.seller_name,
        )

        if existing is not None:
            return existing

        new_seller = Seller(**validated_seller.model_dump())
        return self.repository.add(new_seller)