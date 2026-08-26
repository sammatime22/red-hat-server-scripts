"""Client for interacting with DuckAI API."""

import json
import requests
from typing import Optional
from .response import Response


class DuckAIClient:
    """Client for querying DuckAI."""

    def __init__(
        self,
        model: Optional[str] = None,
        timeout: int = 30,
        mock: bool = False,
        api_endpoint: Optional[str] = None,
        verify_ssl: bool = True
    ):
        """
        Initialize the DuckAI client.

        Args:
            model: The AI model to use (defaults to claude-haiku-4-5)
            timeout: Request timeout in seconds
            mock: If True, uses mock responses (for testing/demo)
            api_endpoint: Custom API endpoint URL (defaults to https://duck.ai/duckchat/v1/chat)
            verify_ssl: If False, skips SSL certificate verification (not recommended for production)
        """
        self.model = model or "claude-haiku-4-5"
        self.timeout = timeout
        self.mock_mode = mock
        self.api_endpoint = api_endpoint or "https://duck.ai/duckchat/v1/chat"
        self.verify_ssl = verify_ssl

        # Create a session with persistent cookies and headers
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self):
        """Configure session with browser-like headers."""
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Referer": "https://duck.ai/",
            "Origin": "https://duck.ai",
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"macOS"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Requested-With": "XMLHttpRequest",
        })

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
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
            "Prefer": "safe"
        }

        payload = {
            "model": self.model,
            "metadata": {
                "toolChoice": {
                    "NewsSearch": False,
                    "VideosSearch": False,
                    "LocalSearch": False,
                    "WeatherForecast": False
                }
            },
            "messages": [
                {"role": "user", "content": question}
            ],
            "canUseTools": True,
            "reasoningEffort": "low",
            "canUseApproxLocation": None,
            "canDelegateImageGeneration": None,
            "durableStream": {
                "messageId": self._generate_uuid(),
                "conversationId": self._generate_uuid(),
                "publicKey": {
                    "alg": "RSA-OAEP-256",
                    "ext": True,
                    "key_ops": ["encrypt"],
                    "kty": "RSA"
                }
            }
        }

        try:
            resp = self.session.post(
                self.api_endpoint,
                json=payload,
                headers=headers,
                timeout=self.timeout,
                stream=True,
                verify=self.verify_ssl
            )

            if resp.status_code == 200:
                return self._parse_stream_response(resp)
            elif resp.status_code == 418:
                # Challenge/verification required (likely DuckDuckGo bot detection)
                error_msg = "DuckAI detected this as automated access. Consider:"
                error_msg += "\n- Using from a browser context"
                error_msg += "\n- Using mock=True for testing"
                error_msg += "\n- Adding proper authentication/session"
                return Response(
                    body=error_msg,
                    status_code=418,
                    raw_data={
                        "error_type": "ERR_CHALLENGE",
                        "message": "Bot challenge detected",
                        "endpoint": self.api_endpoint
                    }
                )
            else:
                error_text = resp.text[:200] if resp.text else f"HTTP {resp.status_code}"
                return Response(
                    body=f"API returned status code {resp.status_code}: {error_text}",
                    status_code=resp.status_code,
                    raw_data={
                        "response_text": error_text,
                        "endpoint": self.api_endpoint
                    }
                )
        except requests.exceptions.Timeout:
            return Response(
                body="Request timeout - the API took too long to respond",
                status_code=504,
                raw_data={"error": "timeout", "endpoint": self.api_endpoint}
            )
        except requests.exceptions.ConnectionError as e:
            return Response(
                body=f"Connection error: {str(e)}",
                status_code=503,
                raw_data={"error": "connection_error", "endpoint": self.api_endpoint}
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def _parse_stream_response(self, response: requests.Response) -> Response:
        """
        Parse a streaming response from DuckAI's /duckchat/v1/chat endpoint.
        Uses Server-Sent Events (SSE) format.

        Args:
            response: The streaming response object

        Returns:
            Response object with accumulated message
        """
        message_content = ""
        chat_title = ""

        try:
            for line in response.iter_lines():
                if not line:
                    continue

                line_str = line.decode('utf-8') if isinstance(line, bytes) else line

                # Handle Server-Sent Events (SSE) format
                if line_str.startswith('data: '):
                    data_str = line_str[6:]  # Remove 'data: ' prefix

                    # Handle end marker
                    if data_str == '[DONE]':
                        break

                    # Handle chat title marker
                    if data_str.startswith('[CHAT_TITLE:'):
                        chat_title = data_str[12:-1]  # Extract title between brackets
                        continue

                    try:
                        data = json.loads(data_str)
                        if isinstance(data, dict):
                            # Extract message content from assistant response
                            if data.get('role') == 'assistant' and 'message' in data:
                                message_content += data['message']
                    except json.JSONDecodeError:
                        # Silently skip non-JSON SSE data
                        pass

            return Response(
                body=message_content or "No response received",
                status_code=200,
                raw_data={
                    "streaming": True,
                    "chat_title": chat_title,
                    "model": self.model
                }
            )
        except Exception as e:
            return Response(
                body=f"Error parsing response: {str(e)}",
                status_code=500,
                raw_data={"error": str(e)}
            )

    def _generate_uuid(self) -> str:
        """Generate a UUID-like string for DuckAI requests."""
        import uuid
        return str(uuid.uuid4())

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


def ask(
    question: str,
    model: Optional[str] = None,
    mock: bool = False,
    api_endpoint: Optional[str] = None,
    verify_ssl: bool = True
) -> Response:
    """
    Ask a question to DuckAI's default model.

    Args:
        question: The question to ask
        model: Optional model to use (uses default if not specified)
        mock: If True, uses mock responses (for testing without network access)
        api_endpoint: Custom API endpoint URL
        verify_ssl: If False, skips SSL certificate verification

    Returns:
        Response object containing the AI's response

    Example:
        >>> import duckai as da
        >>> resp = da.ask("Why did the chicken cross the road?")
        >>> print(resp.body)

        >>> # Using mock mode (for testing)
        >>> resp = da.ask("Why did the chicken cross the road?", mock=True)
        >>> print(resp.body)

        >>> # Using custom endpoint
        >>> resp = da.ask("question", api_endpoint="https://custom.api/chat")
        >>> print(resp.body)
    """
    if mock:
        client = DuckAIClient(model=model, mock=True)
        return client.ask(question)
    elif model or api_endpoint or not verify_ssl:
        client = DuckAIClient(
            model=model,
            api_endpoint=api_endpoint,
            verify_ssl=verify_ssl
        )
        return client.ask(question)
    return _default_client.ask(question)
