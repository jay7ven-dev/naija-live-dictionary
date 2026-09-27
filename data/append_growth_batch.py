#!/usr/bin/env python3
"""Append lexicon-growth batch 2 to dictionary.json without wiping enrichments."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\boija\OneDrive - UMass Lowell") / "'26Hussell shit" / "Pidgin Writng system"
DICT = ROOT / "data" / "dictionary.json"

# Keep in sync with build_seed.py growth batch 2 (2026-09-27).
NEW = [
    {
        "id": "sharp",
        "standard_spelling": "sharp",
        "informal_variants": [],
        "part_of_speech": "adjective",
        "definitions": ["sharp; quick; also intensifier in sharp-sharp"],
        "example_sentences": ["Make we go sharp-sharp."],
    },
    {
        "id": "sef",
        "standard_spelling": "sef",
        "informal_variants": ["self"],
        "part_of_speech": "particle",
        "definitions": ["emphatic particle (even; self)"],
        "example_sentences": ["I sef go go."],
    },
    {
        "id": "nia",
        "standard_spelling": "nia",
        "informal_variants": ["near", "nearby"],
        "part_of_speech": "adverb",
        "definitions": ["near; nearby"],
        "example_sentences": ["Di skul nia."],
    },
    {
        "id": "fut",
        "standard_spelling": "fut",
        "informal_variants": ["foot", "feet"],
        "part_of_speech": "noun",
        "definitions": ["foot; feet"],
        "example_sentences": ["Mai fut de pein."],
    },
    {
        "id": "bele",
        "standard_spelling": "bele",
        "informal_variants": ["beli", "belly", "stomach"],
        "part_of_speech": "noun",
        "definitions": ["belly; stomach"],
        "example_sentences": ["Mai bele don ful."],
    },
    {
        "id": "yam",
        "standard_spelling": "yam",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["yam"],
        "example_sentences": ["I wan chop yam."],
    },
    {
        "id": "egusi",
        "standard_spelling": "egusi",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["egusi (melon-seed soup or stew)"],
        "example_sentences": ["Mama kuk egusi."],
    },
    {
        "id": "okro",
        "standard_spelling": "okro",
        "informal_variants": ["okra"],
        "part_of_speech": "noun",
        "definitions": ["okra"],
        "example_sentences": ["Okro soup sweet."],
    },
    {
        "id": "fisi",
        "standard_spelling": "fisi",
        "informal_variants": ["fish"],
        "part_of_speech": "noun",
        "definitions": ["fish"],
        "example_sentences": ["I wan fisi."],
    },
    {
        "id": "bred",
        "standard_spelling": "bred",
        "informal_variants": ["bread"],
        "part_of_speech": "noun",
        "definitions": ["bread"],
        "example_sentences": ["Buy bred fo mi."],
    },
    {
        "id": "bia",
        "standard_spelling": "bia",
        "informal_variants": ["beer"],
        "part_of_speech": "noun",
        "definitions": ["beer"],
        "example_sentences": ["Im de drink bia."],
    },
    {
        "id": "klaim",
        "standard_spelling": "klaim",
        "informal_variants": ["climb", "klimb"],
        "part_of_speech": "verb",
        "definitions": ["to climb"],
        "example_sentences": ["E klaim di tri."],
    },
    {
        "id": "finis",
        "standard_spelling": "finis",
        "informal_variants": ["finish"],
        "part_of_speech": "verb",
        "definitions": ["to finish"],
        "example_sentences": ["Finis yu wok."],
    },
    {
        "id": "opin",
        "standard_spelling": "opin",
        "informal_variants": ["open"],
        "part_of_speech": "verb",
        "definitions": ["to open"],
        "example_sentences": ["Opin di do."],
    },
    {
        "id": "weit",
        "standard_spelling": "weit",
        "informal_variants": ["wait"],
        "part_of_speech": "verb",
        "definitions": ["to wait"],
        "example_sentences": ["Weit fo mi."],
    },
    {
        "id": "dans",
        "standard_spelling": "dans",
        "informal_variants": ["dance"],
        "part_of_speech": "verb",
        "definitions": ["to dance"],
        "example_sentences": ["Dem de dans."],
    },
    {
        "id": "izi",
        "standard_spelling": "izi",
        "informal_variants": ["easy"],
        "part_of_speech": "adjective",
        "definitions": ["easy"],
        "example_sentences": ["Di wok izi."],
    },
    {
        "id": "hevi",
        "standard_spelling": "hevi",
        "informal_variants": ["heavy"],
        "part_of_speech": "adjective",
        "definitions": ["heavy"],
        "example_sentences": ["Dis bag hevi."],
    },
    {
        "id": "dak",
        "standard_spelling": "dak",
        "informal_variants": ["dark"],
        "part_of_speech": "adjective",
        "definitions": ["dark"],
        "example_sentences": ["Di rum dak."],
    },
    {
        "id": "mornin",
        "standard_spelling": "mornin",
        "informal_variants": ["morning"],
        "part_of_speech": "noun",
        "definitions": ["morning"],
        "example_sentences": ["Gud mornin."],
    },
    {
        "id": "frend",
        "standard_spelling": "frend",
        "informal_variants": ["friend"],
        "part_of_speech": "noun",
        "definitions": ["friend"],
        "example_sentences": ["Im na mai frend."],
    },
    {
        "id": "oga",
        "standard_spelling": "oga",
        "informal_variants": ["boss"],
        "part_of_speech": "noun",
        "definitions": ["boss; sir; master"],
        "example_sentences": ["Oga, abeg help mi."],
    },
]


def main() -> int:
    entries = json.loads(DICT.read_text(encoding="utf-8"))
    by_id = {e["id"] for e in entries}
    added = 0
    for e in NEW:
        if e["id"] in by_id:
            print(f"skip existing id: {e['id']}")
            continue
        std = e["standard_spelling"]
        e["informal_variants"] = [v for v in e.get("informal_variants", []) if v != std]
        entries.append(e)
        by_id.add(e["id"])
        added += 1
    DICT.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added {added} entries; total now {len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
