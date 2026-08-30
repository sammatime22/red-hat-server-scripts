"""DuckAI Python library for querying DuckDuckGo's AI service."""

from .client import ask, DuckAIClient
from .response import Response

__version__ = "0.1.0"
__all__ = ["ask", "DuckAIClient", "Response"]
