#!/usr/bin/env python3
"""Append lexicon-growth batch 8. Idempotent. Does not rebuild the index."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICT = ROOT / "data" / "dictionary.json"

# Corpus misses + the Fix-spelling false hit whine→fain (2026-10-23).
NEW = [
    {
        "id": "wain",
        "standard_spelling": "wain",
        "informal_variants": ["whine"],
        "part_of_speech": "verb",
        "definitions": ["to whine; complain at someone"],
        "example_sentences": ["Yu dé wain mi."],
    },
    {
        "id": "plenti",
        "standard_spelling": "plenti",
        "informal_variants": ["plenty"],
        "part_of_speech": "adjective",
        "definitions": ["plenty; many"],
        "example_sentences": ["Plenti pipul de dia."],
    },
    {
        "id": "sapos",
        "standard_spelling": "sapos",
        "informal_variants": ["suppose"],
        "part_of_speech": "verb",
        "definitions": ["to suppose"],
        "example_sentences": ["Sapos yu go."],
    },
    {
        "id": "veks",
        "standard_spelling": "veks",
        "informal_variants": ["vex"],
        "part_of_speech": "adjective",
        "definitions": ["angry; vexed"],
        "example_sentences": ["I veks."],
    },
    {
        "id": "enitin",
        "standard_spelling": "enitin",
        "informal_variants": ["anyting", "anything"],
        "part_of_speech": "pronoun",
        "definitions": ["anything"],
        "example_sentences": ["Enitin fit hapen."],
    },
    {
        "id": "evritin",
        "standard_spelling": "evritin",
        "informal_variants": ["everyting", "everything"],
        "part_of_speech": "pronoun",
        "definitions": ["everything"],
        "example_sentences": ["Evritin de ok."],
    },
    {
        "id": "sombodi",
        "standard_spelling": "sombodi",
        "informal_variants": ["somebody"],
        "part_of_speech": "pronoun",
        "definitions": ["somebody"],
        "example_sentences": ["Sombodi de dia."],
    },
]


def main() -> int:
    entries = json.loads(DICT.read_text(encoding="utf-8"))
    by_id = {e["id"]: e for e in entries}
    added = 0
    for e in NEW:
        if e["id"] in by_id:
            print(f"skip existing id: {e['id']}")
            continue
        std = e["standard_spelling"]
        e["informal_variants"] = [v for v in e.get("informal_variants", []) if v != std]
        entries.append(e)
        by_id[e["id"]] = e
        added += 1

    ehen = by_id.get("ehen")
    if ehen is None:
        print("missing entry ehen", file=sys.stderr)
        return 1
    variants = ehen.setdefault("informal_variants", [])
    if "ehn" not in variants:
        variants.append("ehn")
        print("mapped ehn -> ehen")
    else:
        print("ehn already on ehen")

    DICT.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added {added} entries; total now {len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
