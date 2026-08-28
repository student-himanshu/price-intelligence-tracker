"""Command-line entry point for the Price Intelligence Tracker."""
import argparse

from price_tracker import __version__
from price_tracker.collectors.factory import create_collector
from price_tracker.database.session import get_session_factory
from price_tracker.pipeline.orchestrator import PipelineOrchestrator


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="price-tracker",
        description="Price Intelligence Tracker CLI.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
    )
    subparsers = parser.add_subparsers(dest="command")
    collect_parser = subparsers.add_parser(
        "collect",
        help="Collect and persist product price data.",
    )
    collect_parser.add_argument(
        "--collector",
        default="demo",
        choices=("demo", "demo_marketplace"),
        help="Collector implementation to use.",
    )
    collect_parser.add_argument(
        "--url",
        help="Product URL required by web-based collectors.",
    )
    return parser
def run_collection(collector_type: str, url: str | None) -> int:
    """Run the selected collector and persist its records."""
    collector = create_collector(
        collector_type,
        url=url,
    )
    session = get_session_factory()()
    try:
        orchestrator = PipelineOrchestrator(
            session=session,
            collector=collector,
        )
        processed = orchestrator.run()
        session.commit()
        return processed
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
def main() -> None:
    """Run the command-line interface."""
    parser = create_parser()
    args = parser.parse_args()
    if args.command == "collect":
        processed = run_collection(
            collector_type=args.collector,
            url=args.url,
        )
        print(f"Processed {processed} record(s).")
if __name__ == "__main__":
    main()
