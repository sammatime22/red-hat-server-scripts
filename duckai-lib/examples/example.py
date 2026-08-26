#!/usr/bin/env python3
"""Example usage of the duckai library with rate limit handling."""

import sys
from pathlib import Path

# Add parent directory to path to allow importing duckai from examples/
sys.path.insert(0, str(Path(__file__).parent.parent))

import duckai as da
import time

def ask_with_rate_limit_handling(question, mock=False, model=None, retry_delay=5):
    """Ask a question with automatic rate limit handling."""
    try:
        response = da.ask(question, mock=mock, model=model)

        if response.status_code == 429:
            print(f"⚠️  Rate limited. Waiting {retry_delay}s before retry...")
            time.sleep(retry_delay)
            return da.ask(question, mock=mock, model=model)

        return response
    except Exception as e:
        print(f"Error: {str(e)}")
        # Fallback to mock mode
        return da.ask(question, mock=True)

def main():
    """Run example queries."""
    print("=== DuckAI Library Examples ===\n")
    print("Note: Examples use mock=True to avoid rate limiting.\n")

    # Example 1: Simple question (mock mode)
    print("Example 1: Simple Question (Mock Mode)")
    print("-" * 40)
    question = "Why did the chicken cross the road?"
    print(f"Q: {question}")
    response = ask_with_rate_limit_handling(question, mock=True)
    print(f"Status: {response.status_code}")
    print(f"Is Mock: {response.raw_data.get('mock', False)}")
    print(f"A: {response.body}\n")

    # Example 2: Different question (mock mode)
    print("Example 2: Different Question (Mock Mode)")
    print("-" * 40)
    question = "What is the capital of France?"
    print(f"Q: {question}")
    response = ask_with_rate_limit_handling(question, mock=True)
    print(f"Status: {response.status_code}")
    print(f"A: {response.body}\n")

    # Example 3: Using a specific model (mock mode)
    print("Example 3: Using Specific Model (Mock Mode)")
    print("-" * 40)
    question = "Explain quantum entanglement briefly"
    print(f"Q: {question}")
    response = ask_with_rate_limit_handling(question, model="gpt-4", mock=True)
    print(f"Status: {response.status_code}")
    print(f"A: {response.body}\n")

    # Example 4: Real API call with rate limit handling
    print("Example 4: Real API Call (With Rate Limit Handling)")
    print("-" * 40)
    question = "Tell me a joke"
    response = ask_with_rate_limit_handling(question, mock=False)
    if response.status_code == 200:
        print(f"Success! Response: {response.body}")
    elif response.status_code == 429:
        print(f"⚠️  Rate limited: {response.body}")
    else:
        print(f"Status: {response.status_code}")
        print(f"Note: {response.body[:100]}...\n")

    # Example 5: Mock mode for instant responses
    print("Example 5: Mock Mode for Testing (Instant)")
    print("-" * 40)
    question = "Tell me a joke"
    response = da.ask(question, mock=True)
    print(f"Q: {question}")
    print(f"Status: {response.status_code} (instant, no API call)")
    print(f"A: {response.body}\n")

    # Example 6: Checking if response is from mock
    print("Example 6: Checking Response Type")
    print("-" * 40)
    response = da.ask("What is Python?", mock=True)
    is_mock = response.raw_data.get("mock", False)
    print(f"Is mock response? {is_mock}")
    print(f"Response: {response.body}")

    # Example 7: Rate limit best practices
    print("\n\nExample 7: Rate Limit Best Practices")
    print("-" * 40)
    print("✓ Use mock=True for testing")
    print("✓ Add delays between real API calls")
    print("✓ Implement exponential backoff for retries")
    print("✓ Handle 429 errors gracefully")
    print("✓ Check response.status_code before using response.body")


if __name__ == "__main__":
    main()
