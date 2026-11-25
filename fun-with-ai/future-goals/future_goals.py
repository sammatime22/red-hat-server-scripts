#!/usr/bin/env python3
"""A tiny script to write down and rank the things you want to do in the future."""

from datetime import date

FILENAME = "my_future_goals.txt"


def ask_rank(goal):
    """Ask for a rank from 1 to 10 until a valid number is entered."""
    while True:
        answer = input(f"  How important is '{goal}'? (1-10, 10 = most important): ").strip()
        if answer.isdigit() and 1 <= int(answer) <= 10:
            return int(answer)
        print("  Please enter a number from 1 to 10.")


def main():
    print("=== My Future Goals ===")
    print("Type the things you want to do or have in the future.")
    print("Press Enter on an empty line when you are done.\n")

    goals = []
    while True:
        goal = input(f"Goal #{len(goals) + 1}: ").strip()
        if not goal:
            break
        rank = ask_rank(goal)
        goals.append((rank, goal))

    if not goals:
        print("No goals entered. Nothing was saved.")
        return

    # Highest rank first
    goals.sort(key=lambda item: item[0], reverse=True)

    with open(FILENAME, "a", encoding="utf-8") as f:
        f.write(f"--- {date.today().isoformat()} ---\n")
        for rank, goal in goals:
            f.write(f"[{rank:>2}/10] {goal}\n")
        f.write("\n")

    print(f"\nYour goals, most important first:")
    for rank, goal in goals:
        print(f"  [{rank:>2}/10] {goal}")
    print(f"\nSaved {len(goals)} goal(s) to {FILENAME}. Good luck!")


if __name__ == "__main__":
    main()
