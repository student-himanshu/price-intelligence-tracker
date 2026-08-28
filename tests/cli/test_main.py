"""Tests for the command-line interface."""
from importlib import import_module
from unittest.mock import MagicMock

from price_tracker.cli.main import create_parser, run_collection

cli_main = import_module("price_tracker.cli.main")
def test_parser_supports_version() -> None:
    """CLI parser should support the version flag."""
    parser = create_parser()
    args = parser.parse_args([])
    assert args.command is None
def test_parser_supports_collect_command() -> None:
    """CLI parser should support the collect command."""
    parser = create_parser()
    args = parser.parse_args(["collect"])
    assert args.command == "collect"
    assert args.collector == "demo"
    assert args.url is None
def test_parser_supports_marketplace_collector() -> None:
    """CLI parser should accept a marketplace collector and URL."""
    parser = create_parser()
    args = parser.parse_args(
        [
            "collect",
            "--collector",
            "demo_marketplace",
            "--url",
            "https://demo.example.com/product",
        ],
    )
    assert args.command == "collect"
    assert args.collector == "demo_marketplace"
    assert args.url == "https://demo.example.com/product"
def test_run_collection_commits_processed_records(monkeypatch) -> None:
    """Collection runner should execute the orchestrator and commit."""
    collector = MagicMock()
    session = MagicMock()
    orchestrator = MagicMock()
    orchestrator.run.return_value = 3
    monkeypatch.setattr(
        cli_main,
        "create_collector",
        lambda collector_type, url=None: collector,
    )
    monkeypatch.setattr(
        cli_main,
        "get_session_factory",
        lambda: lambda: session,
    )
    monkeypatch.setattr(
        cli_main,
        "PipelineOrchestrator",
        lambda session, collector: orchestrator,
    )
    result = run_collection(
        collector_type="demo",
        url=None,
    )
    assert result == 3
    orchestrator.run.assert_called_once_with()
    session.commit.assert_called_once_with()
    session.close.assert_called_once_with()
