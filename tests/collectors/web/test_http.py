"""Tests for the reusable HTTP collector."""
from unittest.mock import MagicMock

import pytest

from price_tracker.collectors.web.http import HttpCollector


def test_http_collector_returns_response_text(monkeypatch) -> None:
    """HTTP collector should return the response body."""
    response = MagicMock()
    response.text = "<html>test</html>"
    monkeypatch.setattr(
        "price_tracker.collectors.web.http.requests.get",
        lambda url, **kwargs: response,
    )
    collector = HttpCollector()
    result = collector.get("https://example.com")
    assert result == "<html>test</html>"
    response.raise_for_status.assert_called_once()
def test_http_collector_passes_timeout_and_headers(monkeypatch) -> None:
    """HTTP collector should pass configured request options."""
    response = MagicMock()
    response.text = "ok"
    requests_get = MagicMock(return_value=response)
    monkeypatch.setattr(
        "price_tracker.collectors.web.http.requests.get",
        requests_get,
    )
    collector = HttpCollector(
        timeout=10.0,
        headers={"User-Agent": "TestAgent"},
    )
    collector.get("https://example.com")
    requests_get.assert_called_once_with(
        "https://example.com",
        headers={"User-Agent": "TestAgent"},
        timeout=10.0,
    )
def test_http_collector_propagates_http_errors(monkeypatch) -> None:
    """HTTP errors should be propagated to the caller."""
    response = MagicMock()
    response.raise_for_status.side_effect = RuntimeError("HTTP error")
    monkeypatch.setattr(
        "price_tracker.collectors.web.http.requests.get",
        lambda url, **kwargs: response,
    )
    collector = HttpCollector()
    with pytest.raises(RuntimeError, match="HTTP error"):
        collector.get("https://example.com")
