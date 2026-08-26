"""Command-line entry point for the Price Intelligence Tracker."""

import argparse

from price_tracker import __version__


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

    return parser


def main() -> None:
    """Run the command-line interface."""
    parser = create_parser()
    parser.parse_args()


if __name__ == "__main__":
    main()