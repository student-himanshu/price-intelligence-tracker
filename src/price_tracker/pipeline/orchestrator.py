"""End-to-end pipeline orchestration."""

from sqlalchemy.orm import Session

from price_tracker.collectors.base import BaseCollector
from price_tracker.pipeline.collector_pipeline import CollectorPipeline
from price_tracker.pipeline.persistence_pipeline import PersistencePipeline


class PipelineOrchestrator:
    """Coordinate collection, normalization, and persistence."""

    def __init__(
        self,
        session: Session,
        collector: BaseCollector,
    ) -> None:
        self.collector_pipeline = CollectorPipeline(collector)
        self.persistence_pipeline = PersistencePipeline(session)

    def run(self) -> int:
        """Run the complete collection and persistence workflow."""
        records = self.collector_pipeline.run()
        return self.persistence_pipeline.persist(records)