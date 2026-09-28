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
        ROOT / "web" / "normalize.html",
        ROOT / "web" / "normalize.js",
        ROOT / "web" / "compose.js",
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

    ime_json = ROOT / "data" / "ime" / "naija-ime-lexicon.json"
    ime_tsv = ROOT / "data" / "ime" / "naija-ime-lexicon.tsv"
    if not ime_json.is_file() or not ime_tsv.is_file():
        print("missing: data/ime/naija-ime-lexicon.json or .tsv (run data/export_ime_lexicon.py)", file=sys.stderr)
        return 1
    ime = json.loads(ime_json.read_text(encoding="utf-8"))
    if ime.get("digraphs") != ["ch", "gb", "sh", "kp", "zh"]:
        print(f"ime digraphs mismatch: {ime.get('digraphs')}", file=sys.stderr)
        return 1
    ime_stale = False
    if len(ime.get("suggestions") or []) != len(index):
        ime_stale = True
        print(
            f"WARN: ime suggestions {len(ime.get('suggestions') or [])} != index {len(index)} "
            "(re-run data/export_ime_lexicon.py when ready)",
            file=sys.stderr,
        )

    kmn = ROOT / "ime" / "keyman" / "naija_sno" / "naija_sno.kmn"
    kps = ROOT / "ime" / "keyman" / "naija_sno" / "naija_sno.kps"
    wordlist = ROOT / "ime" / "keyman" / "naija_sno" / "naija_sno.wordlist.tsv"
    for p in (kmn, kps, wordlist):
        if not p.is_file():
            print(f"missing: {p.relative_to(ROOT)} (II-5b Keyman)", file=sys.stderr)
            return 1
    kmn_text = kmn.read_text(encoding="utf-8")
    for dig in ("gb", "kp", "sh", "ch", "zh"):
        needle = f"'{dig[0]}' + '{dig[1]}' > '{dig}'"
        if needle not in kmn_text:
            print(f"keyman kmn missing digraph: {dig}", file=sys.stderr)
            return 1
    wl_rows = [ln for ln in wordlist.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if len(wl_rows) < 2:
        print("keyman wordlist empty", file=sys.stderr)
        return 1

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

    stale = " (ime stale)" if ime_stale else ""
    print(
        f"OK: {len(entries)} entries, {len(index)} index keys, "
        f"{len(fuzzy.get('terms', []))} fuzzy terms, "
        f"ime export {len(ime['suggestions'])}, "
        f"keyman wordlist {len(wl_rows) - 1}, web + docs layers present{stale}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
