#!/usr/bin/env python3
"""Export digraph + suggestion lexicon for future OS/mobile IMEs (II-5a).

Reads dictionary.json + variant_index.json. Never writes the Live Dictionary.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICT_PATH = ROOT / "data" / "dictionary.json"
INDEX_PATH = ROOT / "data" / "variant_index.json"
OUT_DIR = ROOT / "data" / "ime"
OUT_JSON = OUT_DIR / "naija-ime-lexicon.json"
OUT_TSV = OUT_DIR / "naija-ime-lexicon.tsv"

SCHEMA_VERSION = 1
DIGRAPHS = ["ch", "gb", "sh", "kp", "zh"]
ACUTE_VOWELS = ["á", "é", "í", "ó", "ú"]


def build_package() -> dict:
    entries = json.loads(DICT_PATH.read_text(encoding="utf-8"))
    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    by_id = {e["id"]: e["standard_spelling"] for e in entries}

    suggestions = []
    missing = 0
    for variant, eid in sorted(index.items(), key=lambda x: x[0].casefold()):
        std = by_id.get(eid)
        if std is None:
            missing += 1
            continue
        suggestions.append(
            {"variant": variant, "entry_id": eid, "standard": std}
        )

    if missing:
        print(f"warn: skipped {missing} index keys with unknown entry_id", file=sys.stderr)

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": {
            "dictionary": "data/dictionary.json",
            "variant_index": "data/variant_index.json",
        },
        "counts": {
            "entries": len(entries),
            "index_keys": len(index),
            "suggestions": len(suggestions),
        },
        "digraphs": list(DIGRAPHS),
        "acute_vowels": list(ACUTE_VOWELS),
        "suggestions": suggestions,
    }


def write_export(pkg: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(pkg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["variant\tstandard\tentry_id"]
    for row in pkg["suggestions"]:
        lines.append(f"{row['variant']}\t{row['standard']}\t{row['entry_id']}")
    OUT_TSV.write_text("\n".join(lines) + "\n", encoding="utf-8")


def self_check() -> int:
    if not OUT_JSON.is_file():
        print(f"missing: {OUT_JSON}", file=sys.stderr)
        return 1
    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    pkg = json.loads(OUT_JSON.read_text(encoding="utf-8"))
    errors: list[str] = []
    if pkg.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version want {SCHEMA_VERSION} got {pkg.get('schema_version')}")
    if pkg.get("digraphs") != DIGRAPHS:
        errors.append(f"digraphs mismatch: {pkg.get('digraphs')}")
    if len(pkg.get("digraphs") or []) != 5:
        errors.append("digraph count != 5")
    if pkg.get("acute_vowels") != ACUTE_VOWELS:
        errors.append(f"acute_vowels mismatch: {pkg.get('acute_vowels')}")
    n_sug = len(pkg.get("suggestions") or [])
    if n_sug != len(index):
        # Allow fewer only if unknown ids were skipped at build; require equality when dictionary is consistent
        errors.append(f"suggestions {n_sug} != index keys {len(index)}")
    if not OUT_TSV.is_file():
        errors.append(f"missing: {OUT_TSV}")
    else:
        tsv_lines = OUT_TSV.read_text(encoding="utf-8").splitlines()
        if len(tsv_lines) != n_sug + 1:
            errors.append(f"tsv rows {len(tsv_lines) - 1} != suggestions {n_sug}")
    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1
    print(f"OK: ime export {n_sug} suggestions, {len(DIGRAPHS)} digraphs")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Export IME lexicon package (II-5a).")
    p.add_argument("--self-check", action="store_true", help="Validate existing export")
    args = p.parse_args(argv)
    if args.self_check:
        return self_check()
    pkg = build_package()
    write_export(pkg)
    print(
        f"Wrote {pkg['counts']['suggestions']} suggestions -> {OUT_JSON.relative_to(ROOT)} "
        f"and {OUT_TSV.relative_to(ROOT)}"
    )
    return self_check()


if __name__ == "__main__":
    raise SystemExit(main())
