"""Terminal formatting for the demo. No logic lives here.

Colour is switched off automatically when stdout is not a TTY, and can be
forced off with NO_COLOR=1 -- so piping the demo into a file gives clean text
for the appendix of a write-up.
"""

from __future__ import annotations

import os
import shutil
import sys
from typing import Iterable, Sequence

WIDTH = min(shutil.get_terminal_size((88, 24)).columns, 88)

_USE_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def _c(code: str) -> str:
    return code if _USE_COLOR else ""


DIM = _c("\033[2m")
BOLD = _c("\033[1m")
RED = _c("\033[31m")
GREEN = _c("\033[32m")
YELLOW = _c("\033[33m")
BLUE = _c("\033[36m")
RESET = _c("\033[0m")


def banner(text: str) -> None:
    print(f"\n{YELLOW}{'!' * WIDTH}{RESET}")
    for line in _wrap(text, WIDTH - 4):
        print(f"{YELLOW}! {RESET}{line}")
    print(f"{YELLOW}{'!' * WIDTH}{RESET}")


def act(number: int | str, title: str, subtitle: str = "") -> None:
    print()
    print(f"{BLUE}{'=' * WIDTH}{RESET}")
    print(f"{BOLD}ACT {number}  ·  {title}{RESET}")
    if subtitle:
        for line in _wrap(subtitle, WIDTH):
            print(f"{DIM}{line}{RESET}")
    print(f"{BLUE}{'=' * WIDTH}{RESET}")


def table(rows: Iterable[tuple[str, str]], *, indent: int = 2) -> None:
    rows = list(rows)
    if not rows:
        return
    keyw = max(len(k) for k, _ in rows)
    pad = " " * indent
    for k, v in rows:
        if not v:
            print(f"{pad}{DIM}{k}{RESET}")
        else:
            print(f"{pad}{k.ljust(keyw)}   {BOLD}{v}{RESET}")


def frame(df, *, indent: int = 2, floatfmt: str = "{:.3f}") -> None:
    """Print a small pandas DataFrame without importing a table library."""
    import pandas as pd

    with pd.option_context("display.float_format", floatfmt.format,
                           "display.width", WIDTH,
                           "display.max_columns", 20):
        text = df.to_string(index=False)
    for line in text.splitlines():
        print(" " * indent + line)


def verdict(ok: bool, text: str) -> None:
    mark = f"{GREEN}PASS{RESET}" if ok else f"{RED}FAIL{RESET}"
    print(f"\n  [{mark}] {text}")


def takeaway(text: str) -> None:
    print()
    for line in _wrap(text, WIDTH - 4):
        print(f"  {BOLD}>{RESET} {line}")


def note(text: str) -> None:
    for line in _wrap(text, WIDTH - 4):
        print(f"  {DIM}{line}{RESET}")


def _wrap(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur: list[str] = []
    for w in words:
        if cur and sum(len(x) + 1 for x in cur) + len(w) > width:
            lines.append(" ".join(cur))
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(" ".join(cur))
    return lines or [""]


def compare(label_a: str, label_b: str, rows: Sequence[tuple[str, str, str]]) -> None:
    """Two-column comparison: (metric, value_a, value_b)."""
    keyw = max(len(r[0]) for r in rows)
    aw = max(len(label_a), max(len(r[1]) for r in rows))
    bw = max(len(label_b), max(len(r[2]) for r in rows))
    print(f"  {'':{keyw}}   {DIM}{label_a:>{aw}}   {label_b:>{bw}}{RESET}")
    for k, a, b in rows:
        print(f"  {k:{keyw}}   {a:>{aw}}   {BOLD}{b:>{bw}}{RESET}")
