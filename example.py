#!/usr/bin/env python3
"""Example usage of the duckai library."""

import duckai as da

def main():
    """Run example queries."""
    print("=== DuckAI Library Examples ===\n")

    # Example 1: Simple question
    print("Example 1: Simple Question")
    print("-" * 40)
    question = "Why did the chicken cross the road?"
    print(f"Q: {question}")
    response = da.ask(question)
    print(f"Status: {response.status_code}")
    print(f"A: {response.body}\n")

    # Example 2: Different question
    print("Example 2: Different Question")
    print("-" * 40)
    question = "What is the capital of France?"
    print(f"Q: {question}")
    response = da.ask(question)
    print(f"Status: {response.status_code}")
    print(f"A: {response.body}\n")

    # Example 3: Using a specific model
    print("Example 3: Using Specific Model")
    print("-" * 40)
    question = "Explain quantum entanglement briefly"
    print(f"Q: {question}")
    response = da.ask(question, model="gpt-4")
    print(f"Status: {response.status_code}")
    print(f"A: {response.body}\n")

    # Example 4: Error handling
    print("Example 4: Error Handling")
    print("-" * 40)
    question = "Tell me a joke"
    response = da.ask(question)
    if response.status_code == 200:
        print(f"Success! Response: {response.body}")
    else:
        print(f"Error occurred: {response.body}")


if __name__ == "__main__":
    main()
