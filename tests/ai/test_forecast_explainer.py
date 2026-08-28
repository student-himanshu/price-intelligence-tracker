"""Tests for AI forecast explanations."""
from decimal import Decimal

from price_tracker.ai.forecast_explainer import AIForecastExplainer


class FakeAIService:
    """Fake AI service for deterministic tests."""
    def __init__(self) -> None:
        self.prompt = None
    def generate(self, prompt: str) -> str:
        """Return a deterministic AI response."""
        self.prompt = prompt
        return "AI explanation for the supplied forecast."
def test_ai_forecast_explainer_generates_explanation() -> None:
    """Explainer should delegate forecast analysis to the AI service."""
    ai_service = FakeAIService()
    explainer = AIForecastExplainer(ai_service)
    result = explainer.explain(
        product_name="Apple iPhone 15 128GB",
        current_price=Decimal("59999.00"),
        forecast_price=Decimal("57999.00"),
        price_change=Decimal("-2000.00"),
        trend="decreasing",
        currency="INR",
    )
    assert result == "AI explanation for the supplied forecast."
    assert ai_service.prompt is not None
    assert "Apple iPhone 15 128GB" in ai_service.prompt
    assert "59999.00" in ai_service.prompt
    assert "57999.00" in ai_service.prompt
    assert "decreasing" in ai_service.prompt
def test_ai_forecast_explainer_handles_insufficient_data() -> None:
    """Explainer should avoid AI calls when forecast data is unavailable."""
    ai_service = FakeAIService()
    explainer = AIForecastExplainer(ai_service)
    result = explainer.explain(
        product_name="Apple iPhone 15 128GB",
        current_price=None,
        forecast_price=None,
        price_change=None,
        trend="insufficient_data",
        currency="INR",
    )
    assert result == (
        "There is not enough price history to generate "
        "an AI forecast explanation."
    )
    assert ai_service.prompt is None
