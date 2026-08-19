#!/usr/bin/env python3
"""Validate dictionary entries against schema/entry.schema.json"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "entry.schema.json"
DEFAULT_DATA = ROOT / "data" / "examples" / "entries.json"


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def validate_entries(entries: list, schema: dict) -> list[str]:
    errors: list[str] = []
    props = schema.get("properties", {})
    required = set(schema.get("required", []))
    pos_enum = set(props.get("part_of_speech", {}).get("enum", []))
    seen_ids: set[str] = set()

    for i, entry in enumerate(entries):
        prefix = f"entry[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix}: must be an object")
            continue

        for key in required:
            if key not in entry:
                errors.append(f"{prefix}: missing required field '{key}'")

        extra = set(entry) - set(props)
        if extra:
            errors.append(f"{prefix}: unknown fields {sorted(extra)}")

        eid = entry.get("id")
        if isinstance(eid, str):
            if eid in seen_ids:
                errors.append(f"{prefix}: duplicate id '{eid}'")
            seen_ids.add(eid)

        std = entry.get("standard_spelling")
        variants = entry.get("informal_variants", [])
        if isinstance(std, str) and isinstance(variants, list):
            if std in variants:
                errors.append(f"{prefix}: standard_spelling must not appear in informal_variants")

        pos = entry.get("part_of_speech")
        if isinstance(pos, str) and pos_enum and pos not in pos_enum:
            errors.append(f"{prefix}: invalid part_of_speech '{pos}'")

        for field in ("definitions", "example_sentences"):
            val = entry.get(field)
            if val is not None and (not isinstance(val, list) or not val):
                errors.append(f"{prefix}: '{field}' must be a non-empty array")

    return errors


def main(argv: list[str]) -> int:
    data_path = Path(argv[1]) if len(argv) > 1 else DEFAULT_DATA
    schema = load_json(SCHEMA_PATH)
    entries = load_json(data_path)
    if not isinstance(entries, list):
        print("Data file must be a JSON array of entries", file=sys.stderr)
        return 1

    errors = validate_entries(entries, schema)
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1

    print(f"OK: {len(entries)} entries validated ({data_path.name})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
