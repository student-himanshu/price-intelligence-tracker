"""Tests for the pipeline orchestrator."""

from unittest.mock import MagicMock

from price_tracker.pipeline.orchestrator import PipelineOrchestrator


def test_orchestrator_runs_collection_and_persistence() -> None:
    """Orchestrator should collect records and persist them."""
    session = MagicMock()
    collector = MagicMock()

    orchestrator = PipelineOrchestrator(session, collector)

    records = [
        {
            "name": "apple iphone 15",
            "seller_name": "demo electronics",
            "seller_domain": "demo-electronics.example",
        }
    ]

    orchestrator.collector_pipeline.run = MagicMock(
        return_value=records,
    )
    orchestrator.persistence_pipeline.persist = MagicMock(
        return_value=1,
    )

    result = orchestrator.run()

    assert result == 1
    orchestrator.collector_pipeline.run.assert_called_once_with()
    orchestrator.persistence_pipeline.persist.assert_called_once_with(records)


def test_orchestrator_returns_persistence_count() -> None:
    """Orchestrator should return the count from persistence."""
    session = MagicMock()
    collector = MagicMock()

    orchestrator = PipelineOrchestrator(session, collector)

    records = [
        {"name": "product one"},
        {"name": "product two"},
        {"name": "product three"},
    ]

    orchestrator.collector_pipeline.run = MagicMock(
        return_value=records,
    )
    orchestrator.persistence_pipeline.persist = MagicMock(
        return_value=3,
    )

    result = orchestrator.run()

    assert result == 3