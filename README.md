# DuckAI - Python Library for DuckDuckGo's AI Service

A simple Python library for querying DuckDuckGo's AI service (duck.ai).

## Installation

```bash
pip install -r requirements.txt
python setup.py install
```

Or install in development mode:

```bash
pip install -e .
```

## Quick Start

### Basic Usage (Requires Network Access)

```python
import duckai as da

# Ask a question using the default model
resp = da.ask("Why did the chicken cross the road?")
print(resp.body)
```

### Testing with Mock Mode

```python
import duckai as da

# Use mock mode for testing (no network required)
resp = da.ask("Why did the chicken cross the road?", mock=True)
print(resp.body)
```

## Usage

### Basic Query

```python
import duckai as da

# Simple query
response = da.ask("What is the capital of France?")
print(response.body)
```

### Response Object

The `ask()` function returns a `Response` object with the following attributes:

- `body` (str): The text response from the AI model
- `status_code` (int): HTTP status code
- `raw_data` (dict): The raw API response data

```python
import duckai as da

response = da.ask("Tell me a joke")
print(f"Status: {response.status_code}")
print(f"Response: {response.body}")
print(f"Raw data: {response.raw_data}")
```

### Specifying a Model

```python
import duckai as da

# Use a specific model
response = da.ask("Explain quantum physics", model="gpt-4")
print(response.body)
```

### Advanced: Using the Client Directly

```python
from duckai.client import DuckAIClient

# Create a custom client
client = DuckAIClient(model="gpt-3.5-turbo", timeout=60)

# Ask questions
response = client.ask("What is machine learning?")
print(response.body)
```

## Features

- Simple and intuitive API
- Built-in error handling
- Support for custom models
- Configurable timeout
- Response metadata

## Mock Mode (For Testing Without Network)

The library includes a built-in mock mode for testing when network access to DuckAI is restricted:

```python
import duckai as da

# Use mock mode - returns pre-defined responses
response = da.ask("Why did the chicken cross the road?", mock=True)
print(response.body)

# Check if response is from mock
if response.raw_data.get("mock"):
    print("This is a mock response for testing")
```

### Supported Mock Questions

Mock mode recognizes these keywords and returns relevant responses:
- "chicken" - Classic joke about crossing the road
- "france" - Capital city information
- "quantum" - Quantum entanglement explanation
- "joke" - A programming joke
- "python" - Information about Python
- "ai" - Artificial Intelligence explanation

For other questions, mock mode returns a generic response.

## Error Handling

```python
import duckai as da

response = da.ask("Your question here")

if response.status_code != 200:
    print(f"Error: {response.body}")
else:
    print(response.body)

# Check for network restrictions
if response.raw_data.get("network_restricted"):
    print("Network access is restricted - use mock=True for testing")
```

## Network Restrictions

Some environments (like cloud-based remote execution) may have network policies that prevent direct access to external APIs. In these cases:

1. Use `mock=True` for testing and development
2. Deploy in an environment with proper network access
3. Check your network policy configuration

```python
import duckai as da

# This will fail in restricted environments:
# resp = da.ask("question")

# This will work everywhere:
resp = da.ask("question", mock=True)
```

## Finding the Actual API Endpoint

DuckAI's actual API endpoint structure is not publicly documented. To find it:

### Using Browser DevTools

1. Open https://duck.ai in your browser
2. Open Developer Tools (F12)
3. Go to Network tab
4. Send a chat message
5. Look for network requests to `duck.ai` or `duckduckgo.com`
6. Note the endpoint URL and any authentication headers

### Using the Diagnostic Script

Run the included diagnostic script to test common endpoint patterns:

```bash
python3 test_endpoints.py
```

This will test various endpoint patterns and show which ones respond.

### Using a Custom Endpoint

Once you've found the correct endpoint, use it with the library:

```python
import duckai as da

# Use the endpoint you discovered
resp = da.ask(
    "Your question",
    api_endpoint="https://duck.ai/YOUR_ACTUAL_ENDPOINT",
    verify_ssl=True
)
print(resp.body)
```

## SSL Certificate Verification

By default, SSL certificates are verified. To disable verification (not recommended for production):

```python
import duckai as da

resp = da.ask("question", verify_ssl=False)
```

Or using the client directly:

```python
from duckai.client import DuckAIClient

client = DuckAIClient(verify_ssl=False)
response = client.ask("question")
```

## Requirements

- Python 3.8+
- requests library

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.
