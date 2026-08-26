"""Tests for the API metadata endpoint."""

from fastapi.testclient import TestClient

from price_tracker.api.app import app

client = TestClient(app)


def test_api_metadata() -> None:
    """Metadata endpoint should return API information."""
    response = client.get("/meta")

    assert response.status_code == 200
    assert response.json() == {
        "name": "Price Intelligence Tracker API",
        "version": "0.1.0",
        "status": "ready",
    }