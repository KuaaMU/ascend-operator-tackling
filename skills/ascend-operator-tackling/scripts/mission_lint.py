#!/usr/bin/env python3
"""Check a mission for structural drift, stale handoffs, broken evidence links,
and file-hygiene violations (v2).

Exit 1 on ERROR, 0 otherwise (warnings do not fail).
"""

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
    "HARDSET.md",
    "METRICS.md",
    "INDEX.md",
]
REQUIRED_DIRS = ["evidence", "worklog", "reports", "archive", "scratch", "research", "hard-set"]
PLACEHOLDER_PATTERNS = [
    re.compile(r"\[TODO", re.IGNORECASE),
    re.compile(r"\bTODO\b"),
    re.compile(r"\bTBD\b"),
    re.compile(r"<fill", re.IGNORECASE),
]
HASH_PATTERN = re.compile(r"\b[0-9a-fA-F]{12,64}\b")
RESEARCH_QUOTA = 20  # references/file-hygiene.md: research/ file budget


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
    closed_ids: set[str] = set()
    if candidates.is_file():
        text = candidates.read_text(encoding="utf-8", errors="replace")
        if "| promoted |" in text and "evidence" not in text.lower():
            warnings.append("promoted candidates exist without evidence references")
        for line in text.splitlines():
            if line.startswith("|"):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) >= 2 and cells[1].lower() in {"closed", "close", "killed"}:
                    closed_ids.add(cells[0])

    # --- File-hygiene checks (references/file-hygiene.md) ---
    scratch = mission / "scratch"
    if scratch.is_dir():
        for child in scratch.iterdir():
            if child.is_dir() and child.name in closed_ids:
                errors.append(
                    f"orphan scratch dir for closed candidate: scratch/{child.name} "
                    "(archive or delete it)"
                )

    research = mission / "research"
    if research.is_dir():
        n = sum(1 for p in research.iterdir() if p.is_file())
        if n > RESEARCH_QUOTA:
            warnings.append(
                f"research/ holds {n} files (quota {RESEARCH_QUOTA}); "
                "digest before searching more"
            )

    for stray in mission.glob("*.md"):
        if stray.name not in REQUIRED_FILES:
            warnings.append(f"stray markdown at mission root: {stray.name} (move it or delete it)")

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
