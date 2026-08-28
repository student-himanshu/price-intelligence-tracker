"""HTTP client utilities for web collectors."""
from collections.abc import Mapping

import requests


class HttpCollector:
    """Fetch web pages for collector implementations."""
    def __init__(
        self,
        timeout: float = 15.0,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        self.timeout = timeout
        self.headers = dict(
            headers
            or {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/151.0.0.0 Safari/537.36"
                )
            }
        )
    def get(self, url: str) -> str:
        """Fetch a URL and return its response body."""
        response = requests.get(
            url,
            headers=self.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.text
