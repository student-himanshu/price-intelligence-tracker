"""Groq AI provider implementation."""

from groq import Groq

from price_tracker.ai.config import AISettings
from price_tracker.ai.providers import AIProvider


class GroqProvider(AIProvider):
    """AI provider implementation using Groq."""

    def __init__(self, settings: AISettings) -> None:
        if settings.groq_api_key is None:
            raise ValueError("GROQ_API_KEY is not configured.")

        self.client = Groq(
            api_key=settings.groq_api_key.get_secret_value(),
        )

    def generate(self, prompt: str) -> str:
        """Generate a response using Groq."""
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        content = response.choices[0].message.content

        if content is None:
            raise RuntimeError("Groq returned an empty response.")

        return content