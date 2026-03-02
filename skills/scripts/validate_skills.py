#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_GLOB = "ue5-*"
REQUIRED_FRONTMATTER_KEYS = ("name", "description")
LEGACY_TOKENS = ("ue56-", "ue57x-", "UE56", "UE57X")


def has_utf8_bom(raw: bytes) -> bool:
    return raw.startswith(b"\xef\xbb\xbf")


def parse_frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    block = text[4:end]
    data: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        data[k.strip()] = v.strip()
    return data


def validate_skill_dir(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append(f"{skill_dir}: missing SKILL.md")
        return errors

    raw = skill_md.read_bytes()
    if has_utf8_bom(raw):
        errors.append(f"{skill_md}: UTF-8 BOM detected")
    text = raw.decode("utf-8", errors="replace")

    fm = parse_frontmatter(text)
    if fm is None:
        errors.append(f"{skill_md}: invalid YAML frontmatter delimiters")
        return errors

    for key in REQUIRED_FRONTMATTER_KEYS:
        if not fm.get(key):
            errors.append(f"{skill_md}: missing frontmatter key '{key}'")

    expected_name = skill_dir.name
    actual_name = fm.get("name", "")
    if actual_name != expected_name:
        errors.append(f"{skill_md}: name mismatch (expected '{expected_name}', got '{actual_name}')")

    agents_yaml = skill_dir / "agents" / "openai.yaml"
    if not agents_yaml.exists():
        errors.append(f"{skill_dir}: missing recommended agents/openai.yaml")
    return errors


def find_legacy_tokens(skill_dirs: list[Path]) -> list[str]:
    hits: list[str] = []
    for skill_dir in skill_dirs:
        for p in skill_dir.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix.lower() not in {".md", ".yaml", ".yml", ".py", ".csv", ".txt"}:
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
            for token in LEGACY_TOKENS:
                if token in text:
                    hits.append(f"{p}: contains legacy token '{token}'")
                    break
    return hits


def main() -> int:
    skill_dirs = sorted([p for p in ROOT.glob(SKILL_GLOB) if p.is_dir()])
    if not skill_dirs:
        print("No ue5-* skill directories found.")
        return 2

    errors: list[str] = []
    for skill_dir in skill_dirs:
        errors.extend(validate_skill_dir(skill_dir))
    errors.extend(find_legacy_tokens(skill_dirs))

    if errors:
        print("Validation FAILED:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Validation OK")
    print(f"- skills checked: {len(skill_dirs)}")
    print("- no frontmatter/BOM/legacy-token issues found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
