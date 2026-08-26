"""Unit tests for duckai library."""

import unittest
from duckai.response import Response
from duckai.client import DuckAIClient, ask


class TestResponse(unittest.TestCase):
    """Test Response class."""

    def test_response_creation(self):
        """Test creating a Response object."""
        resp = Response(body="Test response", status_code=200)
        self.assertEqual(resp.body, "Test response")
        self.assertEqual(resp.status_code, 200)

    def test_response_with_raw_data(self):
        """Test Response with raw data."""
        raw_data = {"key": "value"}
        resp = Response(body="Test", status_code=200, raw_data=raw_data)
        self.assertEqual(resp.raw_data, raw_data)

    def test_response_repr(self):
        """Test Response string representation."""
        resp = Response(body="Test response body", status_code=200)
        repr_str = repr(resp)
        self.assertIn("Response", repr_str)
        self.assertIn("200", repr_str)


class TestDuckAIClient(unittest.TestCase):
    """Test DuckAIClient class."""

    def test_client_creation(self):
        """Test creating a client."""
        client = DuckAIClient()
        self.assertIsNotNone(client)
        self.assertEqual(client.timeout, 30)

    def test_client_with_model(self):
        """Test client with custom model."""
        client = DuckAIClient(model="gpt-4")
        self.assertEqual(client.model, "gpt-4")

    def test_client_with_timeout(self):
        """Test client with custom timeout."""
        client = DuckAIClient(timeout=60)
        self.assertEqual(client.timeout, 60)


class TestAskFunction(unittest.TestCase):
    """Test ask function."""

    def test_ask_function_exists(self):
        """Test that ask function exists and is callable."""
        self.assertTrue(callable(ask))

    def test_ask_returns_response(self):
        """Test that ask returns a Response object."""
        # This will make a real API call, so we just check the return type
        result = ask("test question")
        self.assertIsInstance(result, Response)
        self.assertIsNotNone(result.body)
        self.assertIsNotNone(result.status_code)


class TestImports(unittest.TestCase):
    """Test module imports."""

    def test_main_imports(self):
        """Test importing from main module."""
        import duckai
        self.assertTrue(hasattr(duckai, 'ask'))
        self.assertTrue(hasattr(duckai, 'Response'))

    def test_client_import(self):
        """Test importing from client module."""
        from duckai.client import DuckAIClient, ask
        self.assertIsNotNone(DuckAIClient)
        self.assertIsNotNone(ask)

    def test_response_import(self):
        """Test importing from response module."""
        from duckai.response import Response
        self.assertIsNotNone(Response)


if __name__ == "__main__":
    unittest.main()
