#!/usr/bin/env python3
"""Append lexicon-growth batch 9. Idempotent. Does not rebuild the index."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICT = ROOT / "data" / "dictionary.json"

# High-frequency corpus misses (2026-10-25). English function words stay unmapped.
NEW = [
    {
        "id": "pesin",
        "standard_spelling": "pesin",
        "informal_variants": ["person"],
        "part_of_speech": "noun",
        "definitions": ["person"],
        "example_sentences": ["Di pesin don go."],
    },
    {
        "id": "laik",
        "standard_spelling": "laik",
        "informal_variants": ["like"],
        "part_of_speech": "verb",
        "definitions": ["to like"],
        "example_sentences": ["I laik am."],
    },
    {
        "id": "tel",
        "standard_spelling": "tel",
        "informal_variants": ["tell"],
        "part_of_speech": "verb",
        "definitions": ["to tell"],
        "example_sentences": ["Tel mi."],
    },
    {
        "id": "beta",
        "standard_spelling": "beta",
        "informal_variants": ["better"],
        "part_of_speech": "adjective",
        "definitions": ["better"],
        "example_sentences": ["Dis wan beta."],
    },
    {
        "id": "mebi",
        "standard_spelling": "mebi",
        "informal_variants": ["maybe"],
        "part_of_speech": "adverb",
        "definitions": ["maybe"],
        "example_sentences": ["Mebi tumoro."],
    },
    {
        "id": "anoda",
        "standard_spelling": "anoda",
        "informal_variants": ["another", "anoder"],
        "part_of_speech": "determiner",
        "definitions": ["another"],
        "example_sentences": ["Anoda pesin."],
    },
    {
        "id": "oda",
        "standard_spelling": "oda",
        "informal_variants": ["other", "oder"],
        "part_of_speech": "determiner",
        "definitions": ["other"],
        "example_sentences": ["Di oda wan."],
    },
    {
        "id": "andastand",
        "standard_spelling": "andastand",
        "informal_variants": ["understand"],
        "part_of_speech": "verb",
        "definitions": ["to understand"],
        "example_sentences": ["I andastand."],
    },
    {
        "id": "pepe",
        "standard_spelling": "pepe",
        "informal_variants": ["pepper"],
        "part_of_speech": "noun",
        "definitions": ["chili pepper"],
        "example_sentences": ["Di sup get pepe."],
    },
    {
        "id": "mata",
        "standard_spelling": "mata",
        "informal_variants": ["matter"],
        "part_of_speech": "noun",
        "definitions": ["matter; issue"],
        "example_sentences": ["No bi di mata."],
    },
    {
        "id": "nem",
        "standard_spelling": "nem",
        "informal_variants": ["name"],
        "part_of_speech": "noun",
        "definitions": ["name"],
        "example_sentences": ["Wetin bi di nem?"],
    },
    {
        "id": "klas",
        "standard_spelling": "klas",
        "informal_variants": ["class"],
        "part_of_speech": "noun",
        "definitions": ["class; lesson"],
        "example_sentences": ["Di klas don stat."],
    },
    {
        "id": "chenj",
        "standard_spelling": "chenj",
        "informal_variants": ["change"],
        "part_of_speech": "verb",
        "definitions": ["to change"],
        "example_sentences": ["Chenj di moni."],
    },
    {
        "id": "na-im",
        "standard_spelling": "na im",
        "informal_variants": ["naim"],
        "part_of_speech": "phrase",
        "definitions": ["it is; that is the one"],
        "example_sentences": ["Na im e bi."],
    },
]

# Real spellings the tighter fuzzy rule no longer guesses.
VARIANTS = [
    ("wuman", "women"),
    ("dea", "dere"),
    ("mtchew", "mtschew"),
    ("somtin", "someting"),
    ("notin", "noting"),
    ("moto", "motor"),
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
