#!/usr/bin/env python3
"""Test different publicKey formats to find what the API accepts."""

import sys
from pathlib import Path
import requests
import json
import uuid
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/event-stream",
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
    "Content-Type": "application/json",
})

endpoint = "https://duck.ai/duckchat/v1/chat"
question = "Hello"

test_count = 0
def test_payload(name, public_key_config):
    """Test a payload variant."""
    global test_count
    test_count += 1

    # Wait between tests to avoid rate limiting
    if test_count > 1:
        print("\n⏳ Waiting 15 seconds before next test to avoid rate limiting...")
        time.sleep(15)

    print(f"\n{'='*60}")
    print(f"Test {test_count}: {name}")
    print(f"{'='*60}")

    payload = {
        "model": "claude-haiku-4-5",
        "metadata": {
            "toolChoice": {
                "NewsSearch": False,
                "VideosSearch": False,
                "LocalSearch": False,
                "WeatherForecast": False
            }
        },
        "messages": [{"role": "user", "content": question}],
        "canUseTools": True,
        "reasoningEffort": "low",
        "durableStream": {
            "messageId": str(uuid.uuid4()),
            "conversationId": str(uuid.uuid4()),
        }
    }

    if public_key_config is not None:
        payload["durableStream"]["publicKey"] = public_key_config

    print(f"\nPublicKey: {json.dumps(public_key_config, indent=2)}")
    print(f"\nFull Payload: {json.dumps(payload, indent=2, default=str)}")

    try:
        print(f"\nSending request...")
        resp = session.post(endpoint, json=payload, timeout=10, stream=True)
        print(f"\n✓ Status: {resp.status_code}")
        print(f"Response: {resp.text}")

        if resp.status_code == 200:
            print("✅ SUCCESS - API accepted this format!")
        elif resp.status_code == 429:
            print("⚠️  Rate Limited (expected) - but format was accepted")
        elif resp.status_code == 400:
            print("❌ Bad Request - this format is invalid")

        return resp.status_code
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

# Test 1: Current format (the one causing 400)
test_payload("Current format (with key_ops)", {
    "alg": "RSA-OAEP-256",
    "ext": True,
    "key_ops": ["encrypt"],
    "kty": "RSA"
})

# Test 2: Without key_ops (this was 429)
test_payload("Without key_ops", {
    "alg": "RSA-OAEP-256",
    "ext": True,
    "kty": "RSA"
})

# Test 3: Without ext
test_payload("Without ext", {
    "alg": "RSA-OAEP-256",
    "key_ops": ["encrypt"],
    "kty": "RSA"
})

# Test 4: Minimal (just alg)
test_payload("Minimal (just alg)", {
    "alg": "RSA-OAEP-256"
})

# Test 5: No publicKey at all
test_payload("No publicKey", None)

print("\n" + "="*60)
print("publicKey format testing complete")
print("="*60)
print("\nSummary:")
print("- If Test 1 shows ❌ and another shows ⚠️, we found the issue")
print("- The working format should be used in client.py")
print("="*60)
