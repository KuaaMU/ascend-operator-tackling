#!/usr/bin/env python3
"""Check a mission for structural drift, stale handoffs, and broken evidence links."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_FILES = [
    "AGENT.md",
    "STATE.md",
    "TRUTH.md",
    "PLAN.md",
    "REVIEW.md",
    "LESSONS.md",
    "HANDOFF.md",
    "CANDIDATES.md",
    "METRICS.md",
    "INDEX.md",
]
REQUIRED_DIRS = ["evidence", "worklog", "reports", "archive"]
PLACEHOLDER_PATTERNS = [
    re.compile(r"\[TODO", re.IGNORECASE),
    re.compile(r"\bTODO\b"),
    re.compile(r"\bTBD\b"),
    re.compile(r"<fill", re.IGNORECASE),
]
HASH_PATTERN = re.compile(r"\b[0-9a-fA-F]{12,64}\b")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mission")
    parser.add_argument("--allow-placeholders", action="store_true")
    args = parser.parse_args()

    mission = Path(args.mission).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not mission.is_dir():
        print(f"ERROR: mission directory not found: {mission}")
        return 1

    for name in REQUIRED_FILES:
        path = mission / name
        if not path.is_file():
            errors.append(f"missing file: {name}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if not args.allow_placeholders:
            for pattern in PLACEHOLDER_PATTERNS:
                if pattern.search(text):
                    errors.append(f"unresolved placeholder in {name}: {pattern.pattern}")

    for name in REQUIRED_DIRS:
        if not (mission / name).is_dir():
            errors.append(f"missing directory: {name}/")

    state = mission / "STATE.md"
    handoff = mission / "HANDOFF.md"
    if state.is_file() and handoff.is_file():
        if handoff.stat().st_mtime + 1 < state.stat().st_mtime:
            warnings.append("HANDOFF.md is older than STATE.md; refresh the recovery point")
        combined = state.read_text(encoding="utf-8", errors="replace") + handoff.read_text(
            encoding="utf-8", errors="replace"
        )
        if not HASH_PATTERN.search(combined):
            warnings.append("STATE/HANDOFF contain no source or binary hash")

    review = mission / "REVIEW.md"
    if review.is_file():
        text = review.read_text(encoding="utf-8", errors="replace").lower()
        if "pending" in text and "verdict" not in text:
            warnings.append("REVIEW.md still appears to be pending")

    candidates = mission / "CANDIDATES.md"
    if candidates.is_file():
        text = candidates.read_text(encoding="utf-8", errors="replace")
        if "| promoted |" in text and "evidence" not in text.lower():
            warnings.append("promoted candidates exist without evidence references")

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(f"Mission structure OK: {mission}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
