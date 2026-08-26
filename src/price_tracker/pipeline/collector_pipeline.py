"""Pipeline for collecting and normalizing product data."""

from typing import Any

from price_tracker.collectors.base import BaseCollector
from price_tracker.normalization import (
    normalize_domain,
    normalize_product_name,
    normalize_seller_name,
)


class CollectorPipeline:
    """Collect and normalize raw listing data."""

    def __init__(self, collector: BaseCollector) -> None:
        self.collector = collector

    def run(self) -> list[dict[str, Any]]:
        """Collect raw data and normalize relevant fields."""
        records = self.collector.collect()

        normalized_records: list[dict[str, Any]] = []

        for record in records:
            normalized_record = record.copy()

            normalized_record["name"] = normalize_product_name(
                record["name"],
            )
            normalized_record["seller_name"] = normalize_seller_name(
                record["seller_name"],
            )
            normalized_record["seller_domain"] = normalize_domain(
                record["seller_domain"],
            )

            normalized_records.append(normalized_record)

        return normalized_records