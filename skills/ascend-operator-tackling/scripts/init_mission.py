#!/usr/bin/env python3
"""Initialize a long-horizon tackling mission from reusable templates.

v2: domain profile support (--profile), file-hygiene directories
(scratch/, research/, hard-set/).
"""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path


def fill(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mission", required=True, help="Mission directory to initialize")
    parser.add_argument("--goal", required=True, help="Final objective")
    parser.add_argument("--acceptance", required=True, help="Acceptance criteria summary")
    parser.add_argument("--operator", default="unknown", help="Workload name")
    parser.add_argument("--repo", default="unknown", help="Repository or workspace")
    parser.add_argument("--task-doc", default="unknown", help="Task document path or URL")
    parser.add_argument(
        "--profile",
        default="",
        help="Domain profile to load, e.g. ascend-cann (references/profiles/<name>.md)",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite known template files")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parent.parent
    template_dir = skill_root / "assets" / "mission"
    if not template_dir.is_dir():
        parser.error(f"mission templates not found: {template_dir}")

    if args.profile:
        profile_path = skill_root / "references" / "profiles" / f"{args.profile}.md"
        if not profile_path.is_file():
            parser.error(f"profile not found: {profile_path}")

    mission = Path(args.mission).expanduser().resolve()
    mission.mkdir(parents=True, exist_ok=True)
    keep = {"evidence", "worklog", "reports", "archive", "scratch", "research", "hard-set"}
    existing = [p for p in mission.iterdir() if p.name not in keep]
    if existing and not args.force:
        parser.error(f"mission directory is not empty: {mission}; use --force to overwrite templates")

    # File-hygiene directories (references/file-hygiene.md).
    for directory in ("evidence", "worklog", "reports", "archive", "scratch", "research", "hard-set"):
        (mission / directory).mkdir(parents=True, exist_ok=True)

    values = {
        "GOAL": args.goal,
        "ACCEPTANCE": args.acceptance,
        "OPERATOR": args.operator,
        "REPO": args.repo,
        "TASK_DOC": args.task_doc,
        "PROFILE": args.profile or "none (generic kernel)",
        "DATE": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    for source in sorted(template_dir.glob("*.md")):
        text = fill(source.read_text(encoding="utf-8"), values)
        destination = mission / source.name
        if destination.exists() and not args.force:
            parser.error(f"destination exists: {destination}; use --force")
        destination.write_text(text, encoding="utf-8", newline="\n")

    print(f"Initialized mission: {mission}")
    if args.profile:
        print(f"Profile loaded: references/profiles/{args.profile}.md")
    print("Next: read AGENT.md, verify the live environment, then fill PLAN/TRUTH/HANDOFF.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
