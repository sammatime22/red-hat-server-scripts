#!/usr/bin/env python3
"""Simplify payload step by step to find what works."""

import sys
from pathlib import Path
import requests
import json
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

test_num = 0
def test(name, payload, wait=15):
    global test_num
    test_num += 1
    if test_num > 1:
        print(f"\n⏳ Waiting {wait}s...")
        time.sleep(wait)

    print(f"\n{'='*70}")
    print(f"Test {test_num}: {name}")
    print(f"{'='*70}")
    print(json.dumps(payload, indent=2, default=str))

    try:
        resp = session.post(endpoint, json=payload, timeout=10, stream=True)
        print(f"\n→ Status: {resp.status_code} | Response: {resp.text[:300]}")
        return resp.status_code
    except Exception as e:
        print(f"\n→ Error: {str(e)}")
        return None

# Start extremely minimal and add complexity
test("Just model + messages", {
    "model": "claude-haiku-4-5",
    "messages": [{"role": "user", "content": "Hello"}]
})

test("Add metadata", {
    "model": "claude-haiku-4-5",
    "messages": [{"role": "user", "content": "Hello"}],
    "metadata": {"toolChoice": {"NewsSearch": False}}
})

test("Add canUseTools", {
    "model": "claude-haiku-4-5",
    "messages": [{"role": "user", "content": "Hello"}],
    "metadata": {"toolChoice": {"NewsSearch": False}},
    "canUseTools": True
})

test("Add reasoningEffort", {
    "model": "claude-haiku-4-5",
    "messages": [{"role": "user", "content": "Hello"}],
    "metadata": {"toolChoice": {"NewsSearch": False}},
    "canUseTools": True,
    "reasoningEffort": "low"
})

test("Add empty durableStream", {
    "model": "claude-haiku-4-5",
    "messages": [{"role": "user", "content": "Hello"}],
    "metadata": {"toolChoice": {"NewsSearch": False}},
    "canUseTools": True,
    "reasoningEffort": "low",
    "durableStream": {}
})

print("\n" + "="*70)
print("ANALYSIS")
print("="*70)
print("Track which status code appears when:")
print("- 418: Bot detection (missing authentication/complexity)")
print("- 400: Bad request (wrong payload format)")
print("- 429: Rate limited (payload accepted!)")
print("- 200: Success")
print("="*70)
