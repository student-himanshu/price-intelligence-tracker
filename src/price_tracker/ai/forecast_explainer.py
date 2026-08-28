"""AI-powered forecast explanation service."""
from decimal import Decimal
from typing import Protocol

from price_tracker.ai.config import AISettings
from price_tracker.ai.service import AIService


class AITextGenerator(Protocol):
    """Protocol for services that generate AI text."""
    def generate(self, prompt: str) -> str:
        """Generate text from a prompt."""
        ...
class AIForecastExplainer:
    """Generate natural-language explanations for price forecasts."""
    def __init__(
        self,
        service: AITextGenerator | AISettings | None = None,
    ) -> None:
        """Initialize the AI forecast explainer."""
        if service is None:
            self.service = AIService(AISettings())
        elif isinstance(service, AISettings):
            self.service = AIService(service)
        else:
            self.service = service
    def explain(
        self,
        product_name: str,
        current_price: Decimal | None,
        forecast_price: Decimal | None,
        price_change: Decimal | None,
        trend: str,
        currency: str,
    ) -> str:
        """Generate an AI explanation for a price forecast."""
        if current_price is None or forecast_price is None:
            return (
                "There is not enough price history to generate "
                "an AI forecast explanation."
            )
        price_change_text = (
            f"{currency} {price_change:.2f}"
            if price_change is not None
            else "N/A"
        )
        prompt = (
            "Analyze the following product price forecast.\n\n"
            f"Product: {product_name}\n"
            f"Current price: {currency} {current_price:.2f}\n"
            f"Forecast price: {currency} {forecast_price:.2f}\n"
            f"Recent price change: {price_change_text}\n"
            f"Trend: {trend}\n\n"
            "Explain the forecast in 2-3 concise sentences. "
            "Mention whether the price is expected to increase, "
            "decrease, or remain stable. "
            "Do not invent information that is not provided."
        )
        return self.service.generate(prompt)
