"""Price history ORM model."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from price_tracker.database.base import Base
from price_tracker.models.listing import Listing


class PriceHistory(Base):
    """Represent a historical price observation for a listing."""

    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    listing_id: Mapped[int] = mapped_column(
        ForeignKey("listings.id", ondelete="CASCADE"),
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    original_price: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    discount_percentage: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="INR",
        server_default="INR",
    )

    collected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    listing: Mapped[Listing] = relationship(
        backref="price_history",
        lazy="selectin",
    )

    __table_args__ = (
        Index(
            "ix_price_history_listing_collected_at",
            "listing_id",
            "collected_at",
        ),
        Index(
            "ix_price_history_collected_at",
            "collected_at",
        ),
    )