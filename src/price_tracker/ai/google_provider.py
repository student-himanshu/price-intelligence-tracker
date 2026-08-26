"""Google Gemini AI provider implementation."""

from google import genai

from price_tracker.ai.config import AISettings
from price_tracker.ai.providers import AIProvider


class GoogleProvider(AIProvider):
    """AI provider implementation using Google Gemini."""

    def __init__(self, settings: AISettings) -> None:
        if settings.google_api_key is None:
            raise ValueError("GOOGLE_API_KEY is not configured.")

        self.client = genai.Client(
            api_key=settings.google_api_key.get_secret_value(),
        )

    def generate(self, prompt: str) -> str:
        """Generate a response using Google Gemini."""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        if response.text is None:
            raise RuntimeError("Google Gemini returned an empty response.")

        return response.text