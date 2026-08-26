#!/usr/bin/env python3
"""Quick test script for debugging DuckAI requests."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import duckai as da

# Test with debug mode and increased timeout
print("Testing DuckAI with debug output and 120s timeout...")
print("=" * 60)

question = "Why did the chicken cross the road?"
print(f"\nQuestion: {question}\n")

response = da.ask(
    question,
    debug=True,
    timeout=120,
    mock=False
)

print("\n" + "=" * 60)
print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.body}")
if response.raw_data:
    print(f"Raw Data: {response.raw_data}")
