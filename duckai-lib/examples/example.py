#!/usr/bin/env python3
"""Example usage of the duckai library with rate limit handling."""

import sys
from pathlib import Path
import argparse

# Add parent directory to path to allow importing duckai from examples/
sys.path.insert(0, str(Path(__file__).parent.parent))

import duckai as da
import time

def ask_with_rate_limit_handling(question, mock=False, model=None, retry_delay=5, timeout=60, debug=False):
    """Ask a question with automatic rate limit handling."""
    try:
        response = da.ask(question, mock=mock, model=model, timeout=timeout, debug=debug)

        if response.status_code == 429:
            print(f"⚠️  Rate limited. Waiting {retry_delay}s before retry...")
            time.sleep(retry_delay)
            return da.ask(question, mock=mock, model=model, timeout=timeout, debug=debug)

        return response
    except Exception as e:
        print(f"Error: {str(e)}")
        # Fallback to mock mode
        return da.ask(question, mock=True)

def main(use_mock=False, use_debug=False, timeout=60):
    """Run example queries.

    Args:
        use_mock: If True, uses mock responses. If False, uses real API (may rate limit).
        use_debug: If True, shows detailed debug output for troubleshooting.
        timeout: Request timeout in seconds (default: 60).
    """
    print("=== DuckAI Library Examples ===\n")
    mode_str = "mock mode" if use_mock else "real API"
    print(f"Using: {mode_str}")
    print(f"Timeout: {timeout}s")
    if use_debug:
        print("Debug: ENABLED (showing detailed request/response info)")
    if not use_mock:
        print("Note: DuckAI has rate limits. Use --mock for instant responses without rate limiting.")
    if use_mock or use_debug:
        print()

    # Example 1: Simple question
    print("Example 1: Simple Question")
    print("-" * 40)
    question = "Why did the chicken cross the road?"
    print(f"Q: {question}")
    response = ask_with_rate_limit_handling(question, mock=use_mock, timeout=timeout, debug=use_debug)
    print(f"Status: {response.status_code}")
    print(f"Is Mock: {response.raw_data.get('mock', False)}")
    print(f"A: {response.body}\n")

    # Example 2: Different question
    print("Example 2: Different Question")
    print("-" * 40)
    question = "What is the capital of France?"
    print(f"Q: {question}")
    response = ask_with_rate_limit_handling(question, mock=use_mock, timeout=timeout, debug=use_debug)
    print(f"Status: {response.status_code}")
    print(f"A: {response.body}\n")

    # Example 3: Using a specific model
    print("Example 3: Using Specific Model")
    print("-" * 40)
    question = "Explain quantum entanglement briefly"
    print(f"Q: {question}")
    response = ask_with_rate_limit_handling(question, model="gpt-4", mock=use_mock, timeout=timeout, debug=use_debug)
    print(f"Status: {response.status_code}")
    print(f"A: {response.body}\n")

    # Example 4: Another API call with rate limit handling
    print("Example 4: Another Query")
    print("-" * 40)
    question = "Tell me a joke"
    response = ask_with_rate_limit_handling(question, mock=use_mock, timeout=timeout, debug=use_debug)
    if response.status_code == 200:
        print(f"Success! Response: {response.body}")
    elif response.status_code == 429:
        print(f"⚠️  Rate limited: {response.body}")
    else:
        print(f"Status: {response.status_code}")
        print(f"Note: {response.body[:100]}...\n")

    # Example 5: Direct call with mock
    print("Example 5: Direct Mock Call")
    print("-" * 40)
    question = "What is Python?"
    response = da.ask(question, mock=True)
    print(f"Q: {question}")
    print(f"Status: {response.status_code} (always instant with mock=True)")
    print(f"A: {response.body}\n")

    # Example 6: Checking if response is from mock
    print("Example 6: Checking Response Type")
    print("-" * 40)
    response = da.ask("Tell me a joke", mock=True)
    is_mock = response.raw_data.get("mock", False)
    print(f"Is mock response? {is_mock}")
    print(f"Response: {response.body}")

    # Example 7: Best practices
    print("\n\nExample 7: Best Practices")
    print("-" * 40)
    print("✓ Use --mock flag to avoid rate limiting during development")
    print("✓ Add delays between real API calls (5+ seconds recommended)")
    print("✓ Implement exponential backoff for retries")
    print("✓ Handle 429 errors gracefully")
    print("✓ Check response.status_code before using response.body")
    print("✓ Handle 400 Bad Request errors (invalid queries)")
    print("✓ Handle 418 Challenge errors (bot detection)")

    print("\n\nUsage Examples:")
    print("-" * 40)
    print("# Use mock mode (no rate limiting, instant responses):")
    print("python3 example.py --mock\n")
    print("# Use real API (will hit rate limits):")
    print("python3 example.py\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="DuckAI Library Examples",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 example.py              # Use real API (may rate limit)
  python3 example.py --mock       # Use mock mode (instant, no rate limiting)
  python3 example.py --debug      # Show detailed request/response debug info
  python3 example.py --timeout 120  # Increase timeout to 120 seconds
  python3 example.py --mock --debug # Mock mode with debug output
        """
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock responses instead of real API calls"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging (shows detailed request/response info)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Request timeout in seconds (default: 60)"
    )

    args = parser.parse_args()
    main(use_mock=args.mock, use_debug=args.debug, timeout=args.timeout)
