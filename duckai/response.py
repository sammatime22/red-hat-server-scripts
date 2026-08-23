"""Response class for DuckAI API responses."""


class Response:
    """Represents a response from DuckAI."""

    def __init__(self, body: str, status_code: int = 200, raw_data: dict = None):
        """
        Initialize a Response object.

        Args:
            body: The response text from the AI model
            status_code: HTTP status code of the response
            raw_data: The raw response data from the API
        """
        self.body = body
        self.status_code = status_code
        self.raw_data = raw_data or {}

    def __repr__(self):
        return f"Response(status_code={self.status_code}, body={self.body[:50]}...)"
