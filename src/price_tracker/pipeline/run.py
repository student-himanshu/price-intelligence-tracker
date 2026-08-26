"""Run the end-to-end price collection pipeline."""

from price_tracker.collectors.demo import DemoCollector
from price_tracker.pipeline.collector_pipeline import CollectorPipeline


def collect_demo_data() -> list[dict]:
    """Collect and normalize deterministic demo data."""
    collector = DemoCollector()
    pipeline = CollectorPipeline(collector)

    return pipeline.run()