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

```python
import duckai as da

# Ask a question using the default model
resp = da.ask("Why did the chicken cross the road?")
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

## Error Handling

```python
import duckai as da

response = da.ask("Your question here")

if response.status_code != 200:
    print(f"Error: {response.body}")
else:
    print(response.body)
```

## Requirements

- Python 3.8+
- requests library

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.
