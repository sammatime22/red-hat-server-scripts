#!/usr/bin/env python3
"""
Diagnostic script to find the correct DuckAI API endpoint.
Tests various common endpoint patterns used by chat services.
"""

import requests
from typing import List, Tuple

def test_endpoint(endpoint: str, timeout: int = 5) -> Tuple[str, int, str]:
    """Test a single endpoint."""
    try:
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": "test"}]
        }
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json"
        }

        resp = requests.post(
            endpoint,
            json=payload,
            headers=headers,
            timeout=timeout,
            verify=False
        )
        return endpoint, resp.status_code, resp.text[:100] if resp.text else "(empty)"
    except requests.exceptions.Timeout:
        return endpoint, 0, "TIMEOUT"
    except requests.exceptions.ConnectionError as e:
        return endpoint, 0, f"CONNECTION_ERROR: {str(e)[:50]}"
    except Exception as e:
        return endpoint, 0, f"ERROR: {str(e)[:50]}"


def main():
    """Test various endpoint patterns."""
    print("=" * 70)
    print("DuckAI API Endpoint Diagnostic")
    print("=" * 70)
    print()

    endpoints_to_test = [
        # Standard patterns
        "https://duck.ai/api/chat",
        "https://duck.ai/api/v1/chat",
        "https://duck.ai/chat",
        "https://api.duck.ai/chat",
        "https://api.duck.ai/v1/chat",

        # DuckDuckGo patterns
        "https://duckduckgo.com/api/chat",
        "https://duckduckgo.com/api/ai/chat",
        "https://duckduckgo.com/duckchat/v1/chat",

        # OpenAI-compatible patterns
        "https://duck.ai/v1/chat/completions",
        "https://api.duck.ai/v1/chat/completions",

        # WebSocket patterns (for reference)
        # "wss://duck.ai/ws/chat",
        # "wss://duck.ai/api/chat/ws",
    ]

    print(f"Testing {len(endpoints_to_test)} endpoints...\n")

    # Suppress SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    results = []
    for i, endpoint in enumerate(endpoints_to_test, 1):
        print(f"[{i}/{len(endpoints_to_test)}] Testing: {endpoint}")
        status, code, text = test_endpoint(endpoint)
        results.append((status, code, text))
        print(f"  Status: {code if code else 'No response'}")
        if code == 200:
            print(f"  ✓ SUCCESS! Response: {text}")
        elif code > 0:
            print(f"  Response: {text}")
        print()

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)

    successful = [r for r in results if r[1] == 200]
    if successful:
        print("\n✓ Successful endpoints (HTTP 200):")
        for endpoint, code, text in successful:
            print(f"  {endpoint}")
            print(f"    Use: da.ask(\"question\", api_endpoint=\"{endpoint}\")")
    else:
        print("\n✗ No successful endpoints found.")

    # Show endpoints that responded (not timeout/connection error)
    responded = [r for r in results if r[1] > 0 and r[1] != 200]
    if responded:
        print("\nEndpoints that responded (non-200 status):")
        for endpoint, code, text in responded:
            print(f"  {endpoint}: HTTP {code}")

    print("\n" + "=" * 70)
    print("Notes:")
    print("  - DuckAI might use WebSocket instead of HTTP POST")
    print("  - Authentication or headers might be required")
    print("  - Check browser network tab when accessing duck.ai in a browser")
    print("  - The actual endpoint might be different from these patterns")
    print("=" * 70)


if __name__ == "__main__":
    main()
