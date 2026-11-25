#!/usr/bin/env python3
"""A tiny script to write down the things you want to do or have in the future."""

from datetime import date

FILENAME = "my_future_goals.txt"


def main():
    print("=== My Future Goals ===")
    print("Type the things you want to do or have in the future.")
    print("Press Enter on an empty line when you are done.\n")

    goals = []
    while True:
        goal = input(f"Goal #{len(goals) + 1}: ").strip()
        if not goal:
            break
        goals.append(goal)

    if not goals:
        print("No goals entered. Nothing was saved.")
        return

    with open(FILENAME, "a", encoding="utf-8") as f:
        f.write(f"--- {date.today().isoformat()} ---\n")
        for i, goal in enumerate(goals, start=1):
            f.write(f"{i}. {goal}\n")
        f.write("\n")

    print(f"\nSaved {len(goals)} goal(s) to {FILENAME}. Good luck!")


if __name__ == "__main__":
    main()
