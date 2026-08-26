"""Pipeline for persisting collected price data."""

from decimal import Decimal
from typing import Any

from sqlalchemy.orm import Session

from price_tracker.schemas.listing import ListingCreate
from price_tracker.schemas.price_history import PriceHistoryCreate
from price_tracker.schemas.product import ProductCreate
from price_tracker.schemas.seller import SellerCreate
from price_tracker.services.listing_service import ListingService
from price_tracker.services.price_history_service import PriceHistoryService
from price_tracker.services.product_service import ProductService
from price_tracker.services.seller_service import SellerService


class PersistencePipeline:
    """Persist normalized collector records into the database."""

    def __init__(self, session: Session) -> None:
        self.product_service = ProductService(session)
        self.seller_service = SellerService(session)
        self.listing_service = ListingService(session)
        self.price_history_service = PriceHistoryService(session)

    def persist(self, records: list[dict[str, Any]]) -> int:
        """Persist records and return the number of processed records."""
        processed = 0

        for record in records:
            product = self.product_service.get_or_create(
                ProductCreate(
                    brand=record.get("brand"),
                    model=record.get("model"),
                    normalized_name=record["name"],
                    category=record.get("category"),
                ),
            )

            seller = self.seller_service.get_or_create(
                SellerCreate(
                    seller_name=record["seller_name"],
                    domain=record.get("seller_domain"),
                ),
            )

            listing = self.listing_service.get_or_create(
                ListingCreate(
                    product_id=product.id,
                    seller_id=seller.id,
                    url=record["url"],
                    external_product_id=record.get("external_product_id"),
                    availability=record.get("availability", True),
                ),
            )

            self.price_history_service.record(
                PriceHistoryCreate(
                    listing_id=listing.id,
                    price=Decimal(str(record["price"])),
                    original_price=(
                        Decimal(str(record["original_price"]))
                        if record.get("original_price") is not None
                        else None
                    ),
                    currency=record.get("currency", "INR"),
                ),
            )

            processed += 1

        return processed