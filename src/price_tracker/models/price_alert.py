"""Price alert database model."""
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from price_tracker.database.base import Base


class PriceAlert(Base):
    """Store a target price alert for a product."""
    __tablename__ = "price_alerts"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )
    target_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
    triggered_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
    product = relationship(
        "Product",
        back_populates="price_alerts",
    )
