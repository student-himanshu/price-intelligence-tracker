"""Database initialization utilities."""

from price_tracker.database.base import Base
from price_tracker.database.engine import get_engine
from price_tracker.models import Listing, PriceHistory, Product, Seller


def initialize_database() -> None:
    """Create all registered database tables."""
    _ = Listing, PriceHistory, Product, Seller

    engine = get_engine()
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    initialize_database()