#!/usr/bin/env python3
"""
Quickly verify that expected Unreal assets exist in the project tree.
Usage:
  python quick_asset_check.py --root . --asset /Game/BlueprintSaveLoad/Inventory/BP_InventoryPickup
"""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Unreal asset existence by package-style path.")
    parser.add_argument("--root", default=".", help="Project root path")
    parser.add_argument("--asset", action="append", required=True, help="Asset package path, e.g. /Game/Foo/Bar")
    return parser.parse_args()


def package_to_uasset_path(root: Path, package: str) -> Path:
    package = package.strip().strip("/")
    if not package.startswith("Game/"):
        raise ValueError(f"Unsupported package root in '{package}'. Expected '/Game/...'.")
    relative = package[len("Game/") :]
    return root / "Content" / f"{relative}.uasset"


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    missing = []

    print(f"Project root: {root}")
    for package in args.asset:
        try:
            uasset = package_to_uasset_path(root, package)
        except ValueError as exc:
            print(f"[INVALID] {exc}")
            missing.append(package)
            continue

        if uasset.exists():
            print(f"[OK] {package} -> {uasset}")
        else:
            print(f"[MISSING] {package} -> {uasset}")
            missing.append(package)

    if missing:
        print(f"\nMissing/invalid entries: {len(missing)}")
        return 2

    print("\nAll requested assets are present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
