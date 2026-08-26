"""Validation rules for listing data."""

from urllib.parse import urlparse

from price_tracker.schemas.listing import ListingCreate


def validate_listing(listing: ListingCreate) -> ListingCreate:
    """Validate and return a listing schema."""
    parsed_url = urlparse(str(listing.url))

    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise ValueError("Listing URL must be a valid HTTP or HTTPS URL.")

    if listing.external_product_id is not None:
        external_id = listing.external_product_id.strip()

        if not external_id:
            raise ValueError("External product ID cannot be empty.")

        return listing.model_copy(
            update={"external_product_id": external_id},
        )

    return listing