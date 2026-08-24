#!/usr/bin/env python3
"""Example usage of the duckai library."""

import duckai as da

def main():
    """Run example queries."""
    print("=== DuckAI Library Examples ===\n")

    # Example 1: Simple question (mock mode)
    print("Example 1: Simple Question (Mock Mode)")
    print("-" * 40)
    question = "Why did the chicken cross the road?"
    print(f"Q: {question}")
    response = da.ask(question, mock=True)
    print(f"Status: {response.status_code}")
    print(f"A: {response.body}\n")

    # Example 2: Different question (mock mode)
    print("Example 2: Different Question (Mock Mode)")
    print("-" * 40)
    question = "What is the capital of France?"
    print(f"Q: {question}")
    response = da.ask(question, mock=True)
    print(f"Status: {response.status_code}")
    print(f"A: {response.body}\n")

    # Example 3: Using a specific model (mock mode)
    print("Example 3: Using Specific Model (Mock Mode)")
    print("-" * 40)
    question = "Explain quantum entanglement briefly"
    print(f"Q: {question}")
    response = da.ask(question, model="gpt-4", mock=True)
    print(f"Status: {response.status_code}")
    print(f"A: {response.body}\n")

    # Example 4: Error handling and network-restricted environment
    print("Example 4: Real API Call (Network Restricted)")
    print("-" * 40)
    question = "Tell me a joke"
    response = da.ask(question)
    if response.status_code == 200:
        print(f"Success! Response: {response.body}")
    else:
        print(f"Status: {response.status_code}")
        print(f"Note: {response.body[:100]}...\n")

    # Example 5: Using mock mode for testing
    print("Example 5: Mock Mode for Testing")
    print("-" * 40)
    question = "Tell me a joke"
    response = da.ask(question, mock=True)
    print(f"Q: {question}")
    print(f"Status: {response.status_code}")
    print(f"A: {response.body}\n")

    # Example 6: Check if response is from mock
    print("Example 6: Checking Mock Flag")
    print("-" * 40)
    response = da.ask("What is Python?", mock=True)
    is_mock = response.raw_data.get("mock", False)
    print(f"Is mock response? {is_mock}")
    print(f"Response: {response.body}")


if __name__ == "__main__":
    main()
