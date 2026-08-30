"""Client for interacting with DuckAI API."""

import json
import requests
import logging
from typing import Optional
from .response import Response
import base64
import subprocess
import tempfile
import os
import shutil
import uuid
import time

# Configure logging
logger = logging.getLogger(__name__)


class DuckAIClient:
    """Client for querying DuckAI."""

    def __init__(
        self,
        model: Optional[str] = None,
        timeout: int = 60,
        mock: bool = False,
        api_endpoint: Optional[str] = None,
        verify_ssl: bool = True,
        debug: bool = False,
        token_refresh_delay: int = 0
    ):
        """
        Initialize the DuckAI client.

        Args:
            model: The AI model to use (defaults to claude-haiku-4-5)
            timeout: Request timeout in seconds (defaults to 60)
            mock: If True, uses mock responses (for testing/demo)
            api_endpoint: Custom API endpoint URL (defaults to https://duck.ai/duckchat/v1/chat)
            verify_ssl: If False, skips SSL certificate verification (not recommended for production)
            debug: If True, logs detailed request/response information for troubleshooting
            token_refresh_delay: Seconds to wait after token refresh before allowing requests (defaults to 0)

        Note:
            When not in mock mode, the client automatically retrieves an auth token during initialization.
            This happens in the __init__ method before ask() can be called. Use token_refresh_delay to
            add a wait period between token retrieval and when ask() can be used, to help avoid rate limits.
        """
        self.model = model or "claude-haiku-4-5"
        self.timeout = timeout
        self.mock_mode = mock
        self.api_endpoint = api_endpoint or "https://duck.ai/duckchat/v1/chat"
        self.verify_ssl = verify_ssl
        self.debug = debug
        self.token_refresh_delay = token_refresh_delay
        self._vqd_hash = None  # Store the current Vqd-Hash-1 for subsequent requests

        if self.debug:
            logging.basicConfig(level=logging.DEBUG)
            logger.setLevel(logging.DEBUG)
            logger.debug(f"DuckAI Client initialized: model={self.model}, timeout={self.timeout}s, endpoint={self.api_endpoint}")

        # Create a session with persistent cookies and headers
        self.session = requests.Session()
        self._setup_session()

        # Get initial auth token and Vqd-Hash
        if not self.mock_mode:
            self._initialize_session()

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
            "X-DuckDuckGo-Version": "1",
        })

    def _initialize_session(self):
        """Initialize session by getting auth token and initial Vqd-Hash."""
        try:
            # Call auth/token endpoint to get initial session
            auth_url = self.api_endpoint.replace("/chat", "/auth/token")
            resp = self.session.get(auth_url, timeout=self.timeout, verify=self.verify_ssl)

            # Extract Vqd-Hash from response headers for use in future requests
            if "x-vqd-hash-1" in resp.headers:
                self._vqd_hash = resp.headers["x-vqd-hash-1"]
                if self.debug:
                    logger.debug(f"Got initial X-Vqd-Hash-1: {self._vqd_hash[:50]}...")

            # Apply token refresh delay if configured
            if self.token_refresh_delay > 0:
                if self.debug:
                    logger.debug(f"Waiting {self.token_refresh_delay}s after token refresh...")
                time.sleep(self.token_refresh_delay)
        except Exception as e:
            if self.debug:
                logger.debug(f"Failed to initialize session: {e}")
            # Don't fail if initialization doesn't work, continue anyway

    def refresh_token(self) -> bool:
        """
        Manually refresh the authentication token.

        This can be useful to reset the rate limit window or to get a fresh token
        before making a new request. The token is automatically refreshed during
        client initialization, but this method allows manual refresh if needed.

        Returns:
            True if token refresh was successful, False otherwise
        """
        if self.mock_mode:
            if self.debug:
                logger.debug("Token refresh skipped in mock mode")
            return True

        try:
            if self.debug:
                logger.debug("Refreshing authentication token...")

            auth_url = self.api_endpoint.replace("/chat", "/auth/token")
            resp = self.session.get(auth_url, timeout=self.timeout, verify=self.verify_ssl)

            # Extract Vqd-Hash from response headers
            if "x-vqd-hash-1" in resp.headers:
                self._vqd_hash = resp.headers["x-vqd-hash-1"]
                if self.debug:
                    logger.debug(f"Token refreshed successfully")

            # Apply token refresh delay if configured
            if self.token_refresh_delay > 0:
                if self.debug:
                    logger.debug(f"Waiting {self.token_refresh_delay}s after token refresh...")
                time.sleep(self.token_refresh_delay)

            return True
        except Exception as e:
            if self.debug:
                logger.debug(f"Failed to refresh token: {e}")
            return False

    def _generate_dynamic_headers(self) -> dict:
        """Generate dynamic headers that change per request."""
        # Generate journey ID (persistent for session)
        if not hasattr(self, '_journey_id'):
            self._journey_id = uuid.uuid4().hex[:32]

        # Generate x-fe-signals (base64-encoded JSON with timing data)
        start_time = int(time.time() * 1000)
        signals = {
            "start": start_time,
            "events": [
                {"name": "startNewChat_free", "delta": 80},
                {"name": "action", "delta": 670952, "trusted": True}
            ],
            "end": 671962
        }
        x_fe_signals = base64.b64encode(
            json.dumps(signals).encode()
        ).decode()

        headers = {
            "x-fe-version": "serp_20260828_152654_ET-41515a9327d5511bd1d4d6f06d3c3bfe4f03bc62",
            "x-fe-signals": x_fe_signals,
            "x-ddg-journey-id": self._journey_id,
        }

        # Use the stored Vqd-Hash if available
        if self._vqd_hash:
            headers["X-Vqd-Hash-1"] = self._vqd_hash
        else:
            headers["X-Vqd-Hash-1"] = "unknown"

        return headers

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
        # Add dynamic headers for this request
        headers.update(self._generate_dynamic_headers())

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
                "publicKey": self._generate_rsa_public_key()
            }
        }

        if self.debug:
            logger.debug(f"Query: {question}")
            logger.debug(f"Endpoint: {self.api_endpoint}")
            # Show all headers including session headers
            all_headers = {**self.session.headers, **headers}
            logger.debug(f"All Headers: {json.dumps({k: v for k, v in all_headers.items() if k != 'Authorization'}, indent=2)}")
            logger.debug(f"Payload: {json.dumps(payload, indent=2, default=str)}")

        try:
            resp = self.session.post(
                self.api_endpoint,
                json=payload,
                headers=headers,
                timeout=self.timeout,
                stream=True,
                verify=self.verify_ssl
            )

            if self.debug:
                logger.debug(f"Response Status: {resp.status_code}")
                logger.debug(f"Response Headers: {json.dumps(dict(resp.headers), indent=2, default=str)}")

            # Extract and store X-Vqd-Hash-1 for next request
            if "x-vqd-hash-1" in resp.headers:
                self._vqd_hash = resp.headers["x-vqd-hash-1"]
                if self.debug:
                    logger.debug(f"Updated X-Vqd-Hash-1 for next request")

            if resp.status_code == 200:
                return self._parse_stream_response(resp)
            elif resp.status_code == 429:
                # Rate limited - this is actually good (means request was valid)
                error_msg = "Rate limited by DuckAI. Please wait before making another request."
                return Response(
                    body=error_msg,
                    status_code=429,
                    raw_data={
                        "error_type": "ERR_RATE_LIMIT",
                        "message": "Too many requests",
                        "endpoint": self.api_endpoint
                    }
                )
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
                error_text = resp.text if resp.text else f"HTTP {resp.status_code}"
                if self.debug:
                    logger.debug(f"Error Response (full): {error_text}")
                    logger.debug(f"Error Status: {resp.status_code}")
                    try:
                        error_json = resp.json()
                        logger.debug(f"Error JSON: {json.dumps(error_json, indent=2)}")
                    except:
                        pass
                return Response(
                    body=f"API returned status code {resp.status_code}: {error_text[:500]}",
                    status_code=resp.status_code,
                    raw_data={
                        "response_text": error_text[:500],
                        "full_response": error_text,
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

    def _generate_rsa_public_key(self) -> dict:
        """
        Generate an RSA key pair and extract public key components using openssl.

        Returns:
            dict with 'e' (exponent) and 'n' (modulus) in base64url format
        """
        try:
            # Try to find openssl using shutil.which() which properly searches PATH
            openssl_path = shutil.which("openssl")
            if not openssl_path:
                # Fallback to common locations
                for path in ["/usr/bin/openssl", "/bin/openssl", "/usr/local/bin/openssl"]:
                    if os.path.exists(path):
                        openssl_path = path
                        break

            if not openssl_path:
                raise FileNotFoundError("openssl not found in system PATH or common locations")

            # Create temporary directory for keys
            with tempfile.TemporaryDirectory() as tmpdir:
                key_path = os.path.join(tmpdir, "key.pem")
                pubkey_path = os.path.join(tmpdir, "pubkey.pem")

                # Pass environment explicitly to ensure PATH is available
                env = os.environ.copy()

                # Generate private key using openssl
                subprocess.run(
                    [openssl_path, "genrsa", "-out", key_path, "2048"],
                    check=True,
                    capture_output=True,
                    text=True,
                    env=env
                )

                # Extract public key
                subprocess.run(
                    [openssl_path, "rsa", "-in", key_path, "-pubout", "-out", pubkey_path],
                    check=True,
                    capture_output=True,
                    text=True,
                    env=env
                )

                # Extract modulus and exponent from public key
                result = subprocess.run(
                    [openssl_path, "rsa", "-pubin", "-in", pubkey_path, "-text", "-noout"],
                    check=True,
                    capture_output=True,
                    text=True,
                    env=env
                )

                output = result.stdout

                # Parse modulus (n) - it's hex encoded in the output
                n_hex = ""
                in_modulus = False
                for line in output.split('\n'):
                    if 'modulus:' in line.lower():
                        in_modulus = True
                        continue
                    if in_modulus:
                        if line.strip().startswith(('publicExponent:', 'Exponent:')):
                            break
                        # Remove colons and whitespace
                        hex_part = line.strip().replace(':', '').replace(' ', '')
                        if hex_part:
                            n_hex += hex_part

                # Parse exponent (e)
                e_value = None
                for line in output.split('\n'):
                    if 'exponent' in line.lower() or 'Exponent' in line:
                        # Extract the number (typically 65537)
                        parts = line.split()
                        for part in parts:
                            try:
                                e_value = int(part)
                                break
                            except ValueError:
                                pass

                if not e_value:
                    e_value = 65537  # Default RSA exponent

                # Convert hex modulus to base64url
                if n_hex:
                    n_bytes = bytes.fromhex(n_hex)
                    n_b64 = base64.urlsafe_b64encode(n_bytes).decode('utf-8').rstrip('=')
                else:
                    raise ValueError("Could not extract modulus from openssl output")

                # Convert exponent to base64url
                e_bytes = e_value.to_bytes(
                    (e_value.bit_length() + 7) // 8, byteorder='big'
                )
                e_b64 = base64.urlsafe_b64encode(e_bytes).decode('utf-8').rstrip('=')

                return {
                    "e": e_b64,
                    "n": n_b64,
                    "use": "enc"
                }
        except Exception as e:
            logger.error(f"Failed to generate RSA public key: {e}")
            # Fallback: return a reasonable default structure
            # Note: This will likely result in 400 error from API, but prevents crashes
            return {
                "alg": "RSA-OAEP-256",
                "kty": "RSA",
                "use": "enc"
            }

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
    verify_ssl: bool = True,
    timeout: int = 60,
    debug: bool = False,
    token_refresh_delay: int = 0
) -> Response:
    """
    Ask a question to DuckAI's default model.

    Args:
        question: The question to ask
        model: Optional model to use (uses default if not specified)
        mock: If True, uses mock responses (for testing without network access)
        api_endpoint: Custom API endpoint URL
        verify_ssl: If False, skips SSL certificate verification
        timeout: Request timeout in seconds (default: 60)
        debug: If True, logs detailed request/response info for troubleshooting
        token_refresh_delay: Seconds to wait after token refresh before allowing requests (default: 0)

    Returns:
        Response object containing the AI's response

    Example:
        >>> import duckai as da
        >>> resp = da.ask("Why did the chicken cross the road?")
        >>> print(resp.body)

        >>> # Using mock mode (for testing)
        >>> resp = da.ask("Why did the chicken cross the road?", mock=True)
        >>> print(resp.body)

        >>> # Using debug mode (for troubleshooting)
        >>> resp = da.ask("question", debug=True)
        >>> print(resp.body)

        >>> # Using custom endpoint
        >>> resp = da.ask("question", api_endpoint="https://custom.api/chat")
        >>> print(resp.body)

        >>> # Using token refresh delay (to avoid rate limits)
        >>> resp = da.ask("question", token_refresh_delay=5)
        >>> print(resp.body)
    """
    if mock:
        client = DuckAIClient(model=model, mock=True, debug=debug)
        return client.ask(question)
    elif model or api_endpoint or not verify_ssl or timeout != 60 or debug or token_refresh_delay != 0:
        client = DuckAIClient(
            model=model,
            api_endpoint=api_endpoint,
            verify_ssl=verify_ssl,
            timeout=timeout,
            debug=debug,
            token_refresh_delay=token_refresh_delay
        )
        return client.ask(question)
    return _default_client.ask(question)
