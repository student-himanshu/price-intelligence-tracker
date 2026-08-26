"""Product listing ORM model."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from price_tracker.database.base import Base
from price_tracker.models.product import Product
from price_tracker.models.seller import Seller


class Listing(Base):
    """Represent a product listing offered by a seller."""

    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )

    seller_id: Mapped[int] = mapped_column(
        ForeignKey("sellers.id", ondelete="CASCADE"),
        nullable=False,
    )

    url: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    external_product_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    availability: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    product: Mapped[Product] = relationship(
        backref="listings",
        lazy="selectin",
    )

    seller: Mapped[Seller] = relationship(
        backref="listings",
        lazy="selectin",
    )

    __table_args__ = (
        UniqueConstraint(
            "seller_id",
            "external_product_id",
            name="uq_listing_seller_external_product",
        ),
        Index("ix_listings_product_id", "product_id"),
        Index("ix_listings_seller_id", "seller_id"),
        Index("ix_listings_availability", "availability"),
    )