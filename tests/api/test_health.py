"""Tests for the health API endpoint."""

from fastapi.testclient import TestClient

from price_tracker.api.app import app

client = TestClient(app)


def test_health_check() -> None:
    """Health endpoint should return an OK response."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "price-intelligence-tracker",
    }