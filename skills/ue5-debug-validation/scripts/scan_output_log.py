#!/usr/bin/env python3
"""
Scan Unreal log files and summarize Error/Warning counts by category.
Usage:
  python scan_output_log.py --log Saved/Logs/BlueprintRuntimeSavingand.log --top 20
"""

from __future__ import annotations

import argparse
import collections
import re
from pathlib import Path


LINE_RE = re.compile(
    r"^\[[^\]]+\]\[(?P<frame>\s*\d+)\](?P<verbosity>\w+):\s*(?P<category>[^:]+):\s*(?P<message>.*)$"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize Unreal log warnings/errors.")
    parser.add_argument("--log", required=True, help="Path to Unreal .log file")
    parser.add_argument("--top", type=int, default=20, help="Top categories to print")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    log_path = Path(args.log)
    if not log_path.exists():
        print(f"[ERROR] Log file not found: {log_path}")
        return 1

    totals = collections.Counter()
    by_category = collections.Counter()

    with log_path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            m = LINE_RE.match(line.strip())
            if not m:
                continue
            verbosity = m.group("verbosity")
            category = m.group("category").strip()
            if verbosity not in {"Warning", "Error"}:
                continue
            totals[verbosity] += 1
            by_category[(verbosity, category)] += 1

    print(f"Log: {log_path}")
    print(f"Errors: {totals['Error']}")
    print(f"Warnings: {totals['Warning']}")
    print("")
    print("Top categories:")
    for (verbosity, category), count in by_category.most_common(args.top):
        print(f"- {verbosity:<7} {category}: {count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
