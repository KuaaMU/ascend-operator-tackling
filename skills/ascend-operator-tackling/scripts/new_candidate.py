#!/usr/bin/env python3
"""Append one falsifiable optimization candidate to a mission ledger."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


def clean(value: str) -> str:
    return " ".join(value.replace("|", "\\|").split())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mission", required=True)
    parser.add_argument("--candidate", default="", help="Stable candidate ID")
    parser.add_argument("--owner", default="unassigned")
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--hypothesis", required=True)
    parser.add_argument("--change", required=True, help="The single variable to change")
    parser.add_argument("--prediction", required=True)
    parser.add_argument("--kill-criterion", required=True)
    parser.add_argument("--evidence", default="pending")
    parser.add_argument("--status", default="proposed")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    mission = Path(args.mission).expanduser().resolve()
    if not mission.is_dir():
        parser.error(f"mission directory not found: {mission}")

    candidate = args.candidate.strip() or "C-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    ledger = mission / "CANDIDATES.md"
    if not ledger.exists():
        ledger.write_text(
            "# Candidates\n\n"
            "| ID | Status | Owner | Baseline | Hypothesis | Single Variable | Prediction | "
            "Kill Criterion | Evidence | Decision | Reopen Condition |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|\n",
            encoding="utf-8",
        )

    row = (
        f"| {clean(candidate)} | {clean(args.status)} | {clean(args.owner)} | "
        f"{clean(args.baseline)} | {clean(args.hypothesis)} | {clean(args.change)} | "
        f"{clean(args.prediction)} | {clean(args.kill_criterion)} | {clean(args.evidence)} | "
        "pending | pending |\n"
    )
    if args.dry_run:
        print(row, end="")
        return 0

    with ledger.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(row)
    print(f"Appended candidate {candidate} to {ledger}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

