"""DuckAI Python library for querying DuckDuckGo's AI service."""

from .client import ask
from .response import Response

__version__ = "0.1.0"
__all__ = ["ask", "Response"]
