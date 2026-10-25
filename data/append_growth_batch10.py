#!/usr/bin/env python3
"""Append lexicon-growth batch 10. Idempotent. Does not rebuild the index."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICT = ROOT / "data" / "dictionary.json"

# Next corpus misses after batch 9 (2026-10-25). Function words stay unmapped.
NEW = [
    {
        "id": "dia",
        "standard_spelling": "dia",
        "informal_variants": ["their", "deir"],
        "part_of_speech": "pronoun",
        "definitions": ["their"],
        "example_sentences": ["Na dia moto."],
    },
    {
        "id": "doz",
        "standard_spelling": "doz",
        "informal_variants": ["those", "dose"],
        "part_of_speech": "determiner",
        "definitions": ["those"],
        "example_sentences": ["Doz pesin."],
    },
    {
        "id": "diz",
        "standard_spelling": "diz",
        "informal_variants": ["these", "dese"],
        "part_of_speech": "determiner",
        "definitions": ["these"],
        "example_sentences": ["Diz wan."],
    },
    {
        "id": "nobodi",
        "standard_spelling": "nobodi",
        "informal_variants": ["nobody"],
        "part_of_speech": "pronoun",
        "definitions": ["nobody"],
        "example_sentences": ["Nobodi de dea."],
    },
    {
        "id": "gree",
        "standard_spelling": "gree",
        "informal_variants": ["agree"],
        "part_of_speech": "verb",
        "definitions": ["to agree"],
        "example_sentences": ["Abeg gree."],
    },
    {
        "id": "klot",
        "standard_spelling": "klot",
        "informal_variants": ["cloth"],
        "part_of_speech": "noun",
        "definitions": ["cloth; clothes"],
        "example_sentences": ["Di klot red."],
    },
    {
        "id": "suffa",
        "standard_spelling": "suffa",
        "informal_variants": ["suffer"],
        "part_of_speech": "verb",
        "definitions": ["to suffer"],
        "example_sentences": ["I dé suffa."],
    },
    {
        "id": "pawa",
        "standard_spelling": "pawa",
        "informal_variants": ["power"],
        "part_of_speech": "noun",
        "definitions": ["power"],
        "example_sentences": ["Pawa don go."],
    },
    {
        "id": "sirios",
        "standard_spelling": "sirios",
        "informal_variants": ["serious"],
        "part_of_speech": "adjective",
        "definitions": ["serious"],
        "example_sentences": ["Na sirios mata."],
    },
    {
        "id": "biliv",
        "standard_spelling": "biliv",
        "informal_variants": ["believe"],
        "part_of_speech": "verb",
        "definitions": ["to believe"],
        "example_sentences": ["I biliv am."],
    },
    {
        "id": "wori",
        "standard_spelling": "wori",
        "informal_variants": ["worry"],
        "part_of_speech": "verb",
        "definitions": ["to worry"],
        "example_sentences": ["No wori."],
    },
    {
        "id": "fil",
        "standard_spelling": "fil",
        "informal_variants": ["feel"],
        "part_of_speech": "verb",
        "definitions": ["to feel"],
        "example_sentences": ["I fil am."],
    },
    {
        "id": "stori",
        "standard_spelling": "stori",
        "informal_variants": ["story"],
        "part_of_speech": "noun",
        "definitions": ["story"],
        "example_sentences": ["Tel mi di stori."],
    },
    {
        "id": "wach",
        "standard_spelling": "wach",
        "informal_variants": ["watch"],
        "part_of_speech": "verb",
        "definitions": ["to watch"],
        "example_sentences": ["Wach am."],
    },
    {
        "id": "leta",
        "standard_spelling": "leta",
        "informal_variants": ["later"],
        "part_of_speech": "adverb",
        "definitions": ["later"],
        "example_sentences": ["Wi go leta."],
    },
    {
        "id": "mari",
        "standard_spelling": "mari",
        "informal_variants": ["marry"],
        "part_of_speech": "verb",
        "definitions": ["to marry"],
        "example_sentences": ["Dem wan mari."],
    },
    {
        "id": "fes",
        "standard_spelling": "fes",
        "informal_variants": ["face"],
        "part_of_speech": "noun",
        "definitions": ["face"],
        "example_sentences": ["Wash di fes."],
    },
    {
        "id": "maind",
        "standard_spelling": "maind",
        "informal_variants": ["mind"],
        "part_of_speech": "noun",
        "definitions": ["mind"],
        "example_sentences": ["Chenj di maind."],
    },
    {
        "id": "ova",
        "standard_spelling": "ova",
        "informal_variants": ["over"],
        "part_of_speech": "preposition",
        "definitions": ["over"],
        "example_sentences": ["E don ova."],
    },
    {
        "id": "side",
        "standard_spelling": "side",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["side"],
        "example_sentences": ["Di oda side."],
    },
    {
        "id": "boil",
        "standard_spelling": "boil",
        "informal_variants": [],
        "part_of_speech": "verb",
        "definitions": ["to boil"],
        "example_sentences": ["Boil di wota."],
    },
    {
        "id": "join",
        "standard_spelling": "join",
        "informal_variants": [],
        "part_of_speech": "verb",
        "definitions": ["to join"],
        "example_sentences": ["Join wi."],
    },
]

VARIANTS = [
    ("somtin", "tins"),
    ("somtin", "things"),
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

    for eid, variant in VARIANTS:
        entry = by_id.get(eid)
        if entry is None:
            print(f"missing entry {eid}", file=sys.stderr)
            return 1
        variants = entry.setdefault("informal_variants", [])
        if variant not in variants and variant != entry["standard_spelling"]:
            variants.append(variant)
            print(f"mapped {variant} -> {eid}")
        else:
            print(f"already {variant} -> {eid}")

    DICT.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added {added} entries; total now {len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
