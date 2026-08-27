#!/usr/bin/env python3
"""Test different payload variations to find what causes 400 errors."""

import sys
from pathlib import Path
import requests
import json
import uuid

sys.path.insert(0, str(Path(__file__).parent.parent))

# Setup session with headers
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
    print(f"Payload: {json.dumps(payload, indent=2, default=str)}")

    try:
        resp = session.post(endpoint, json=payload, timeout=10, stream=True)
        print(f"\nStatus: {resp.status_code}")
        if resp.status_code != 200:
            print(f"Response: {resp.text}")
        return resp.status_code
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Test 1: Minimal payload
test_payload("Minimal", {
    "model": "claude-haiku-4-5",
    "messages": [{"role": "user", "content": question}],
})

# Test 2: With metadata
test_payload("With metadata", {
    "model": "claude-haiku-4-5",
    "metadata": {"toolChoice": {"NewsSearch": False}},
    "messages": [{"role": "user", "content": question}],
})

# Test 3: Full payload without null values
test_payload("Full without nulls", {
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
        "publicKey": {
            "alg": "RSA-OAEP-256",
            "ext": True,
            "key_ops": ["encrypt"],
            "kty": "RSA"
        }
    }
})

# Test 4: Without reasoningEffort
test_payload("Without reasoningEffort", {
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
    "durableStream": {
        "messageId": str(uuid.uuid4()),
        "conversationId": str(uuid.uuid4()),
        "publicKey": {
            "alg": "RSA-OAEP-256",
            "ext": True,
            "key_ops": ["encrypt"],
            "kty": "RSA"
        }
    }
})

# Test 5: Without canUseTools
test_payload("Without canUseTools", {
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
    "reasoningEffort": "low",
    "durableStream": {
        "messageId": str(uuid.uuid4()),
        "conversationId": str(uuid.uuid4()),
        "publicKey": {
            "alg": "RSA-OAEP-256",
            "ext": True,
            "key_ops": ["encrypt"],
            "kty": "RSA"
        }
    }
})

# Test 6: Without durableStream
test_payload("Without durableStream", {
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
})

print("\n" + "="*60)
print("Payload testing complete. Check results above.")
print("="*60)
