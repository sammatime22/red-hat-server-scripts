"""Client for interacting with DuckAI API."""

import json
import requests
from typing import Optional
from .response import Response


class DuckAIClient:
    """Client for querying DuckAI."""

    def __init__(self, model: Optional[str] = None, timeout: int = 30, mock: bool = False):
        """
        Initialize the DuckAI client.

        Args:
            model: The AI model to use (defaults to DuckAI's default)
            timeout: Request timeout in seconds
            mock: If True, uses mock responses (for testing/demo without network access)
        """
        self.model = model or "gpt-4o-mini"
        self.timeout = timeout
        self.base_url = "https://duckduckgo.com"
        self.mock_mode = mock

    def ask(self, question: str) -> Response:
        """
        Ask a question to DuckAI.

        Args:
            question: The question to ask

        Returns:
            Response object containing the AI's response
        """
        if self.mock_mode:
            return self._get_mock_response(question)

        try:
            response = self._query_api(question)
            return response
        except Exception as e:
            error_msg = str(e)
            # Check if it's a network/proxy error
            if "Proxy" in error_msg or "Connection" in error_msg or "403" in error_msg:
                return Response(
                    body=f"Network error: This environment has network restrictions. "
                          f"Use mock=True for testing. Error: {error_msg}",
                    status_code=503,
                    raw_data={"error": error_msg, "network_restricted": True}
                )
            return Response(
                body=f"Error querying DuckAI: {error_msg}",
                status_code=500,
                raw_data={"error": error_msg}
            )

    def _query_api(self, question: str) -> Response:
        """
        Query the DuckAI API using streaming.

        Args:
            question: The question to ask

        Returns:
            Response object
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": question}
            ]
        }

        try:
            resp = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                headers=headers,
                timeout=self.timeout,
                stream=True
            )

            if resp.status_code == 200:
                return self._parse_stream_response(resp)
            else:
                error_text = resp.text or f"HTTP {resp.status_code}"
                return Response(
                    body=f"API returned status code {resp.status_code}: {error_text}",
                    status_code=resp.status_code,
                    raw_data={"response_text": error_text}
                )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def _parse_stream_response(self, response: requests.Response) -> Response:
        """
        Parse a streaming response from DuckAI.

        Args:
            response: The streaming response object

        Returns:
            Response object with accumulated message
        """
        message_content = ""

        try:
            for line in response.iter_lines():
                if not line:
                    continue

                line_str = line.decode('utf-8') if isinstance(line, bytes) else line

                # Handle Server-Sent Events (SSE) format
                if line_str.startswith('data: '):
                    data_str = line_str[6:]  # Remove 'data: ' prefix
                    if data_str == '[DONE]':
                        break

                    try:
                        data = json.loads(data_str)
                        if isinstance(data, dict):
                            # Handle different response formats
                            if 'message' in data:
                                message_content += data['message']
                            elif 'choices' in data and len(data['choices']) > 0:
                                delta = data['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    message_content += delta['content']
                    except json.JSONDecodeError:
                        pass

            return Response(
                body=message_content or "No response received",
                status_code=200,
                raw_data={"streaming": True}
            )
        except Exception as e:
            return Response(
                body=f"Error parsing response: {str(e)}",
                status_code=500,
                raw_data={"error": str(e)}
            )

    def _get_mock_response(self, question: str) -> Response:
        """
        Generate a mock response (for testing without network access).

        Args:
            question: The question asked

        Returns:
            Response object with a mock answer
        """
        mock_responses = {
            "chicken": "The chicken crossed the road to get to the other side! This classic joke plays on the absurdity of explaining an obvious action.",
            "france": "Paris is the capital of France. It's known as the City of Light and is famous for landmarks like the Eiffel Tower.",
            "quantum": "Quantum entanglement is a phenomenon where two or more particles become correlated such that the quantum state of one particle depends on the state of the other, regardless of distance.",
            "joke": "Why don't scientists trust atoms? Because they make up everything!",
            "python": "Python is a high-level, interpreted programming language known for its simplicity and readability. Created by Guido van Rossum.",
            "ai": "Artificial Intelligence (AI) refers to computer systems designed to perform tasks that typically require human intelligence.",
        }

        # Try to match the question to a mock response
        question_lower = question.lower()
        for keyword, response_text in mock_responses.items():
            if keyword in question_lower:
                return Response(
                    body=response_text,
                    status_code=200,
                    raw_data={
                        "mock": True,
                        "model": self.model,
                        "question": question
                    }
                )

        # Default generic response
        return Response(
            body=f"This is a mock response to your question: '{question}'. "
                 f"In production, this would be answered by the {self.model} model via DuckAI API.",
            status_code=200,
            raw_data={
                "mock": True,
                "model": self.model,
                "question": question
            }
        )


_default_client = DuckAIClient()
_mock_client = DuckAIClient(mock=True)


def ask(question: str, model: Optional[str] = None, mock: bool = False) -> Response:
    """
    Ask a question to DuckAI's default model.

    Args:
        question: The question to ask
        model: Optional model to use (uses default if not specified)
        mock: If True, uses mock responses (for testing without network access)

    Returns:
        Response object containing the AI's response

    Example:
        >>> import duckai as da
        >>> resp = da.ask("Why did the chicken cross the road?")
        >>> print(resp.body)

        >>> # Using mock mode (for testing)
        >>> resp = da.ask("Why did the chicken cross the road?", mock=True)
        >>> print(resp.body)
    """
    if mock:
        client = DuckAIClient(model=model, mock=True)
        return client.ask(question)
    elif model:
        client = DuckAIClient(model=model)
        return client.ask(question)
    return _default_client.ask(question)
