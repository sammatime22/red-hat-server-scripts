"""Client for interacting with DuckAI API."""

import json
import requests
from typing import Optional
from .response import Response


class DuckAIClient:
    """Client for querying DuckAI."""

    def __init__(self, model: Optional[str] = None, timeout: int = 30):
        """
        Initialize the DuckAI client.

        Args:
            model: The AI model to use (defaults to DuckAI's default)
            timeout: Request timeout in seconds
        """
        self.model = model
        self.timeout = timeout
        self.base_url = "https://duckduckgo.com"
        self.chat_endpoint = f"{self.base_url}/duckchat/v1/status"

    def ask(self, question: str) -> Response:
        """
        Ask a question to DuckAI.

        Args:
            question: The question to ask

        Returns:
            Response object containing the AI's response
        """
        try:
            response = self._query_api(question)
            return response
        except Exception as e:
            return Response(
                body=f"Error querying DuckAI: {str(e)}",
                status_code=500,
                raw_data={"error": str(e)}
            )

    def _query_api(self, question: str) -> Response:
        """
        Query the DuckAI API.

        Args:
            question: The question to ask

        Returns:
            Response object
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        payload = {
            "query": question,
            "model": self.model or "gpt-3.5-turbo"
        }

        try:
            resp = requests.post(
                f"{self.base_url}/duckchat/v1/chat",
                json=payload,
                headers=headers,
                timeout=self.timeout
            )

            if resp.status_code == 200:
                data = resp.json()
                body = data.get("message", "")
                return Response(body=body, status_code=200, raw_data=data)
            else:
                return Response(
                    body=f"API returned status code {resp.status_code}",
                    status_code=resp.status_code,
                    raw_data={"response_text": resp.text}
                )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")


_default_client = DuckAIClient()


def ask(question: str, model: Optional[str] = None) -> Response:
    """
    Ask a question to DuckAI's default model.

    Args:
        question: The question to ask
        model: Optional model to use (uses default if not specified)

    Returns:
        Response object containing the AI's response

    Example:
        >>> import duckai as da
        >>> resp = da.ask("Why did the chicken cross the road?")
        >>> print(resp.body)
    """
    if model:
        client = DuckAIClient(model=model)
        return client.ask(question)
    return _default_client.ask(question)
