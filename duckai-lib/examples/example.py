#!/usr/bin/env python3
"""Example usage of the duckai library with rate limit handling."""

import sys
from pathlib import Path
import argparse

# Add parent directory to path to allow importing duckai from examples/
sys.path.insert(0, str(Path(__file__).parent.parent))

import duckai as da
import time

def ask_with_rate_limit_handling(question, mock=False, model=None, retry_delay=5, timeout=60, debug=False, token_refresh_delay=0):
    """Ask a question with automatic rate limit handling."""
    try:
        response = da.ask(question, mock=mock, model=model, timeout=timeout, debug=debug, token_refresh_delay=token_refresh_delay)

        if response.status_code == 429:
            print(f"⚠️  Rate limited. Waiting {retry_delay}s before retry...")
            time.sleep(retry_delay)
            return da.ask(question, mock=mock, model=model, timeout=timeout, debug=debug, token_refresh_delay=token_refresh_delay)

        return response
    except Exception as e:
        print(f"Error: {str(e)}")
        # Fallback to mock mode
        return da.ask(question, mock=True)

def main(use_mock=False, use_debug=False, timeout=60, retry_delay=5, token_refresh_delay=0):
    """Run example queries.

    Args:
        use_mock: If True, uses mock responses. If False, uses real API (may rate limit).
        use_debug: If True, shows detailed debug output for troubleshooting.
        timeout: Request timeout in seconds (default: 60).
        retry_delay: Delay between retries on 429 rate limit (default: 5).
        token_refresh_delay: Delay after token refresh before allowing requests (default: 0).
    """
    print("=== DuckAI Library Examples ===\n")
    mode_str = "mock mode" if use_mock else "real API"
    print(f"Using: {mode_str}")
    print(f"Timeout: {timeout}s")
    print(f"Retry Delay: {retry_delay}s")
    if token_refresh_delay > 0:
        print(f"Token Refresh Delay: {token_refresh_delay}s")
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
    response = ask_with_rate_limit_handling(question, mock=use_mock, timeout=timeout, debug=use_debug, retry_delay=retry_delay, token_refresh_delay=token_refresh_delay)
    print(f"Status: {response.status_code}")
    print(f"Is Mock: {response.raw_data.get('mock', False)}")
    print(f"A: {response.body}\n")

    # Example 2: Different question
    print("Example 2: Different Question")
    print("-" * 40)
    question = "What is the capital of France?"
    print(f"Q: {question}")
    response = ask_with_rate_limit_handling(question, mock=use_mock, timeout=timeout, debug=use_debug, retry_delay=retry_delay, token_refresh_delay=token_refresh_delay)
    print(f"Status: {response.status_code}")
    print(f"A: {response.body}\n")

    # Example 3: Using a specific model
    print("Example 3: Using Specific Model")
    print("-" * 40)
    question = "Explain quantum entanglement briefly"
    print(f"Q: {question}")
    response = ask_with_rate_limit_handling(question, model="gpt-4", mock=use_mock, timeout=timeout, debug=use_debug, retry_delay=retry_delay, token_refresh_delay=token_refresh_delay)
    print(f"Status: {response.status_code}")
    print(f"A: {response.body}\n")

    # Example 4: Another API call with rate limit handling
    print("Example 4: Another Query")
    print("-" * 40)
    question = "Tell me a joke"
    response = ask_with_rate_limit_handling(question, mock=use_mock, timeout=timeout, debug=use_debug, retry_delay=retry_delay, token_refresh_delay=token_refresh_delay)
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

    # Example 7: Using token_refresh_delay to avoid rate limits
    print("Example 7: Using Token Refresh Delay")
    print("-" * 40)
    print("The token_refresh_delay parameter adds a wait period after token")
    print("retrieval (during client initialization) before requests can be made.")
    print("This can help avoid immediate rate limiting on first request.\n")
    if not use_mock:
        print("Creating client with 3 second token refresh delay...")
        client = da.DuckAIClient(token_refresh_delay=3, debug=use_debug)
        print("✓ Client initialized and token refresh delay applied")
        print("  (Now safe to call client.ask() without immediate rate limiting)")
        print("  In practice, you would call: response = client.ask('question')\n")
    else:
        print("(Skipping in mock mode - use --mock with token_refresh_delay to test)\n")

    # Example 8: Manual token refresh
    print("Example 8: Manual Token Refresh")
    print("-" * 40)
    print("Use the refresh_token() method to manually get a fresh auth token.")
    print("This is useful if you want to reset rate limit counters between requests.\n")
    if not use_mock:
        print("Creating client...")
        client = da.DuckAIClient(debug=use_debug)
        print("✓ Client initialized with initial token")
        print("\nManually refreshing token...")
        success = client.refresh_token()
        if success:
            print("✓ Token refreshed successfully")
            print("  Ready to make another API call: response = client.ask('question')\n")
        else:
            print("✗ Token refresh failed (may be network issue)\n")
    else:
        print("(In mock mode - manual refresh returns True immediately)\n")

    # Example 9: Best practices
    print("Example 9: Best Practices")
    print("-" * 40)
    print("✓ Use --mock flag to avoid rate limiting during development")
    print("✓ Add delays between real API calls (5+ seconds recommended)")
    print("✓ Use token_refresh_delay parameter for automatic delay on init")
    print("✓ Call refresh_token() manually between requests if needed")
    print("✓ Implement exponential backoff for retries")
    print("✓ Handle 429 errors gracefully")
    print("✓ Check response.status_code before using response.body")
    print("✓ Handle 400 Bad Request errors (invalid queries)")
    print("✓ Handle 418 Challenge errors (bot detection)")

    print("\n\nUsage Examples:")
    print("-" * 40)
    print("# Use mock mode (no rate limiting, instant responses):")
    print("python3 example.py --mock\n")
    print("# Use real API with token refresh delay (helps avoid rate limits):")
    print("python3 example.py --token-refresh-delay 3\n")
    print("# Use real API (will hit rate limits without delay):")
    print("python3 example.py\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="DuckAI Library Examples",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 example.py                    # Use real API (may rate limit)
  python3 example.py --mock             # Use mock mode (instant, no rate limiting)
  python3 example.py --debug            # Show detailed request/response debug info
  python3 example.py --timeout 120      # Increase timeout to 120 seconds
  python3 example.py --retry-delay 10   # Wait 10s between retries on rate limit
  python3 example.py --token-refresh-delay 5  # Wait 5s after token refresh
  python3 example.py --mock --debug     # Mock mode with debug output
  python3 example.py --token-refresh-delay 3 --timeout 120  # Custom delays
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
    parser.add_argument(
        "--retry-delay",
        type=int,
        default=5,
        help="Delay in seconds between retries on rate limit (default: 5)"
    )
    parser.add_argument(
        "--token-refresh-delay",
        type=int,
        default=0,
        help="Delay in seconds after token refresh before allowing requests (default: 0)"
    )

    args = parser.parse_args()
    main(use_mock=args.mock, use_debug=args.debug, timeout=args.timeout, retry_delay=args.retry_delay, token_refresh_delay=args.token_refresh_delay)
