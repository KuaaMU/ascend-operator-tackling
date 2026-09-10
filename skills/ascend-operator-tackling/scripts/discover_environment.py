#!/usr/bin/env python3
"""Read-only discovery of Ascend/CANN tools, compilers, devices, and versions."""

from __future__ import annotations

import argparse
import glob
import json
import os
import platform
import shutil
import subprocess
from pathlib import Path


TOOLS = [
    ("git", ["--version"]),
    ("cmake", ["--version"]),
    ("ninja", ["--version"]),
    ("make", ["--version"]),
    ("g++", ["--version"]),
    ("clang++", ["--version"]),
    ("python3", ["--version"]),
    ("python", ["--version"]),
    ("bisheng", ["--version"]),
    ("ascendc", ["--version"]),
    ("ccec", ["--version"]),
    ("npu-smi", ["--version"]),
    ("msprof", ["--version"]),
    ("mssanitizer", ["--version"]),
    ("msdebug", ["--version"]),
    ("msopgen", ["--version"]),
]
ENV_KEYS = [
    "ASCEND_HOME_PATH",
    "ASCEND_TOOLKIT_HOME",
    "ASCEND_OPP_PATH",
    "ASCEND_CANN_PACKAGE_PATH",
    "ASCEND_AICPU_PATH",
    "PATH",
]


def command_output(command: list[str], timeout: int) -> dict[str, object]:
    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"ok": False, "error": str(exc)}
    text = (result.stdout or result.stderr or "").strip()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return {
        "ok": result.returncode == 0,
        "returncode": result.returncode,
        "output": lines[:5],
    }


def discover(timeout: int, probe: bool) -> dict[str, object]:
    tools: dict[str, object] = {}
    for name, version_args in TOOLS:
        path = shutil.which(name)
        tools[name] = {"path": path}
        if path:
            tools[name]["version"] = command_output([path, *version_args], timeout)

    env = {key: os.environ.get(key, "") for key in ENV_KEYS}
    devices = sorted(glob.glob("/dev/davinci*") + glob.glob("/dev/hisi_hdc"))
    result: dict[str, object] = {
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
        "cwd": str(Path.cwd()),
        "environment": env,
        "devices": devices,
        "tools": tools,
    }

    if probe and shutil.which("npu-smi"):
        result["probe"] = {
            "npu-smi info": command_output([shutil.which("npu-smi") or "npu-smi", "info"], timeout),
        }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=int, default=8)
    parser.add_argument("--probe", action="store_true", help="Run read-only device status commands")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--output", help="Write the report to a file")
    args = parser.parse_args()

    report = discover(max(1, args.timeout), args.probe)
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        Path(args.output).expanduser().write_text(text, encoding="utf-8", newline="\n")
    if args.json or args.output:
        print(text, end="")
    else:
        print(f"Platform: {report['platform']}")
        print(f"Devices: {', '.join(report['devices']) or 'none found'}")
        print("Tools:")
        for name, info in report["tools"].items():
            path = info.get("path") or "-"
            version = info.get("version") or {}
            first = version.get("output", [""])[0] if isinstance(version, dict) else ""
            print(f"  {name:14} path={path} version={first}")
        if "probe" in report:
            print("Probe:")
            for name, output in report["probe"].items():
                print(f"  {name}: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

