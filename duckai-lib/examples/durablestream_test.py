#!/usr/bin/env python3
"""Test different durableStream variations to find the correct format."""

import sys
from pathlib import Path
import requests
import json
import uuid

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

def test_payload(name, payload):
    """Test a payload variant."""
    print(f"\n{'='*60}")
    print(f"Test: {name}")
    print(f"{'='*60}")
    print(f"DurableStream: {json.dumps(payload.get('durableStream'), indent=2, default=str)}")

    try:
        resp = session.post(endpoint, json=payload, timeout=10, stream=True)
        print(f"Status: {resp.status_code} - {resp.text[:200]}")
        return resp.status_code
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Base payload
base = {
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
}

# Test 1: Current format
payload1 = {**base, "durableStream": {
    "messageId": str(uuid.uuid4()),
    "conversationId": str(uuid.uuid4()),
    "publicKey": {
        "alg": "RSA-OAEP-256",
        "ext": True,
        "key_ops": ["encrypt"],
        "kty": "RSA"
    }
}}
test_payload("Current format (UUID strings)", payload1)

# Test 2: Without publicKey
payload2 = {**base, "durableStream": {
    "messageId": str(uuid.uuid4()),
    "conversationId": str(uuid.uuid4()),
}}
test_payload("Without publicKey", payload2)

# Test 3: With only messageId
payload3 = {**base, "durableStream": {
    "messageId": str(uuid.uuid4()),
}}
test_payload("Only messageId", payload3)

# Test 4: With only conversationId
payload4 = {**base, "durableStream": {
    "conversationId": str(uuid.uuid4()),
}}
test_payload("Only conversationId", payload4)

# Test 5: Empty durableStream
payload5 = {**base, "durableStream": {}}
test_payload("Empty durableStream", payload5)

# Test 6: publicKey only (minimal)
payload6 = {**base, "durableStream": {
    "publicKey": {
        "alg": "RSA-OAEP-256",
        "ext": True,
        "key_ops": ["encrypt"],
        "kty": "RSA"
    }
}}
test_payload("PublicKey only", payload6)

# Test 7: Different publicKey format (no key_ops)
payload7 = {**base, "durableStream": {
    "messageId": str(uuid.uuid4()),
    "conversationId": str(uuid.uuid4()),
    "publicKey": {
        "alg": "RSA-OAEP-256",
        "ext": True,
        "kty": "RSA"
    }
}}
test_payload("PublicKey without key_ops", payload7)

# Test 8: Simple publicKey (minimal fields)
payload8 = {**base, "durableStream": {
    "messageId": str(uuid.uuid4()),
    "conversationId": str(uuid.uuid4()),
    "publicKey": {
        "alg": "RSA-OAEP-256",
    }
}}
test_payload("Minimal publicKey", payload8)

print("\n" + "="*60)
print("durableStream testing complete")
print("="*60)
