#!/usr/bin/env python3
"""Stage menu — pick a scenario, pick broken or fixed, run it.

    python stage.py

For when you would rather not type a module path in front of an audience. Every
scenario runs twice: once the way most harnesses measure, once measured
honestly. Nothing here calls an API or needs a network.

Non-interactive equivalents, if you prefer flags on stage:

    python -m judge_audit.scenarios 1
    python -m judge_audit.scenarios 1 --fix
    python -m judge_audit.demo --act 2
"""

from __future__ import annotations

import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from judge_audit.scenarios import SCENARIOS, main as run_scenario  # noqa: E402

USE_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def c(code: str) -> str:
    return code if USE_COLOR else ""


BOLD, DIM, RED, GREEN, BLUE, RESET = (
    c("\033[1m"), c("\033[2m"), c("\033[31m"), c("\033[32m"), c("\033[36m"), c("\033[0m")
)
WIDTH = min(shutil.get_terminal_size((80, 24)).columns, 78)

ROWS = [
    (1, "Repeatability", "one pass, reported as fact", "three passes, spread reported"),
    (2, "Hidden blanks", "unparseable rows dropped", "blanks retried and kept"),
    (3, "Agreement", "a bare 75%", "chance-corrected, with the baseline"),
    (4, "Confident and wrong", "graded judge alone", "graded + binary, and decision risk"),
]


def banner() -> None:
    print()
    print(f"{BLUE}{'=' * WIDTH}{RESET}")
    print(f"{BOLD}  judge-audit — live demo selector{RESET}")
    print(f"{DIM}  Your LLM judge is probably lying to you. Let's check.{RESET}")
    print(f"{BLUE}{'=' * WIDTH}{RESET}\n")
    print(f"  {DIM}{'#':<3} {'scenario':<22} {'broken':<28} fixed{RESET}")
    for n, name, bad, good in ROWS:
        print(f"  {BOLD}{n:<3}{RESET} {name:<22} {RED}{bad:<28}{RESET} {GREEN}{good}{RESET}")
    print(f"  {BOLD}a{RESET}   {'all four':<22} {DIM}runs every scenario in order{RESET}")
    print(f"  {BOLD}q{RESET}   {'quit':<22}")
    print()


def ask(prompt: str, allowed: set[str]) -> str:
    while True:
        try:
            raw = input(prompt).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return "q"
        if raw in allowed:
            return raw
        print(f"  {DIM}pick one of: {', '.join(sorted(allowed))}{RESET}")


def main() -> int:
    while True:
        banner()
        choice = ask("  scenario > ", {"1", "2", "3", "4", "a", "q"})
        if choice == "q":
            print("  bye\n")
            return 0

        mode = ask(f"  {RED}b{RESET}roken or {GREEN}f{RESET}ixed > ", {"b", "f", "q"})
        if mode == "q":
            print("  bye\n")
            return 0

        argv = ["all" if choice == "a" else choice]
        if mode == "f":
            argv.append("--fix")
        print()
        run_scenario(argv)

        again = ask(f"  {DIM}enter to continue, q to quit > {RESET}", {"", "q"})
        if again == "q":
            print("  bye\n")
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
