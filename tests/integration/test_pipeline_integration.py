"""Integration tests for the complete price collection pipeline."""
from sqlalchemy import delete

from price_tracker.collectors.demo import DemoCollector
from price_tracker.database.base import Base
from price_tracker.database.engine import get_engine
from price_tracker.database.session import get_session_factory
from price_tracker.models import (
    Listing,
    PriceAlert,
    PriceHistory,
    Product,
    Seller,
)
from price_tracker.pipeline.orchestrator import PipelineOrchestrator


def _cleanup_demo_data() -> None:
    """Remove demo pipeline data from the integration database."""
    session = get_session_factory()()
    try:
        session.execute(delete(PriceAlert))
        session.execute(delete(PriceHistory))
        session.execute(delete(Listing))
        session.execute(delete(Product))
        session.execute(delete(Seller))
        session.commit()
    finally:
        session.close()
def test_demo_pipeline_persists_records() -> None:
    """Demo collector should persist all collected records into MySQL."""
    _cleanup_demo_data()
    engine = get_engine()
    session = get_session_factory()()
    try:
        Base.metadata.create_all(bind=engine)
        orchestrator = PipelineOrchestrator(
            session=session,
            collector=DemoCollector(),
        )
        processed = orchestrator.run()
        session.commit()
        assert processed == 3
        assert session.query(Product).count() == 3
        assert session.query(Seller).count() == 2
        assert session.query(Listing).count() == 3
        assert session.query(PriceHistory).count() == 3
    finally:
        session.rollback()
        session.close()
        _cleanup_demo_data()
def test_demo_pipeline_creates_expected_products() -> None:
    """Demo pipeline should persist the expected product names."""
    _cleanup_demo_data()
    session = get_session_factory()()
    try:
        orchestrator = PipelineOrchestrator(
            session=session,
            collector=DemoCollector(),
        )
        orchestrator.run()
        session.commit()
        names = {
            product.normalized_name
            for product in session.query(Product).all()
        }
        assert names == {
            "apple iphone 15 128gb",
            "samsung galaxy s24 256gb",
            "oneplus 12 256gb",
        }
    finally:
        session.rollback()
        session.close()
        _cleanup_demo_data()
