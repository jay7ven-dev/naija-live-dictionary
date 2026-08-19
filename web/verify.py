#!/usr/bin/env python3
"""Verify web UI data files exist and variant lookup works."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    dict_path = ROOT / "data" / "dictionary.json"
    index_path = ROOT / "data" / "variant_index.json"
    fuzzy_path = ROOT / "data" / "fuzzy_lookup.json"
    for p in (
        dict_path,
        index_path,
        fuzzy_path,
        ROOT / "web" / "index.html",
        ROOT / "web" / "app.js",
        ROOT / "web" / "docs" / "index.html",
        ROOT / "web" / "docs" / "user" / "index.html",
        ROOT / "web" / "docs" / "ifra" / "index.html",
        ROOT / "web" / "docs" / "repro" / "index.html",
        ROOT / "web" / "docs" / "tutorials" / "index.html",
        ROOT / "docs" / "manuscripts" / "naija-live-dictionary.md",
    ):
        if not p.is_file():
            print(f"missing: {p}", file=sys.stderr)
            return 1

    entries = json.loads(dict_path.read_text(encoding="utf-8"))
    index = json.loads(index_path.read_text(encoding="utf-8"))
    fuzzy = json.loads(fuzzy_path.read_text(encoding="utf-8"))
    by_id = {e["id"]: e for e in entries}

    def resolve(variant: str) -> str | None:
        return index.get(variant) or index.get(variant.lower())

    checks = [
        ("pickin", "pikin"),
        ("book", "buk"),
        ("dey", "de-copula"),
    ]
    for variant, expected_id in checks:
        got = resolve(variant)
        if got != expected_id:
            print(f"lookup fail: {variant!r} -> {got!r}, want {expected_id!r}", file=sys.stderr)
            return 1
        if expected_id not in by_id:
            print(f"missing entry id {expected_id}", file=sys.stderr)
            return 1

    print(
        f"OK: {len(entries)} entries, {len(index)} index keys, "
        f"{len(fuzzy.get('terms', []))} fuzzy terms, web + docs layers present"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
