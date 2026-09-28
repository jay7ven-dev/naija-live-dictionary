#!/usr/bin/env python3
"""Append lexicon-growth batch 5 to dictionary.json without wiping enrichments."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICT = ROOT / "data" / "dictionary.json"

# Lexicon growth batch 5 — slang, food, transport (2026-09-27). No IME/Keyman refresh.
NEW = [
    {
        "id": "oya",
        "standard_spelling": "oya",
        "informal_variants": [],
        "part_of_speech": "interjection",
        "definitions": ["come on; let's go; hurry"],
        "example_sentences": ["Oya make we go."],
    },
    {
        "id": "japa",
        "standard_spelling": "japa",
        "informal_variants": [],
        "part_of_speech": "verb",
        "definitions": ["to flee; emigrate quickly; escape"],
        "example_sentences": ["Plenti pipul don japa."],
    },
    {
        "id": "hustle",
        "standard_spelling": "hustle",
        "informal_variants": [],
        "part_of_speech": "verb",
        "definitions": ["to work hard for money; grind"],
        "example_sentences": ["I de hustle every day."],
    },
    {
        "id": "gbese",
        "standard_spelling": "gbese",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["debt"],
        "example_sentences": ["Gbese don plenti."],
    },
    {
        "id": "fashi",
        "standard_spelling": "fashi",
        "informal_variants": ["fashion"],
        "part_of_speech": "verb",
        "definitions": ["to ignore; leave alone; forget about"],
        "example_sentences": ["Fashi am."],
    },
    {
        "id": "para",
        "standard_spelling": "para",
        "informal_variants": [],
        "part_of_speech": "verb",
        "definitions": ["to get angry; overreact"],
        "example_sentences": ["No para."],
    },
    {
        "id": "lamba",
        "standard_spelling": "lamba",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["lie; false story"],
        "example_sentences": ["Na lamba."],
    },
    {
        "id": "kolo",
        "standard_spelling": "kolo",
        "informal_variants": [],
        "part_of_speech": "adjective",
        "definitions": ["crazy; mad"],
        "example_sentences": ["Di ting kolo."],
    },
    {
        "id": "wuruwuru",
        "standard_spelling": "wuruwuru",
        "informal_variants": ["wuru-wuru"],
        "part_of_speech": "noun",
        "definitions": ["fraud; shady dealing"],
        "example_sentences": ["No do wuruwuru."],
    },
    {
        "id": "haba",
        "standard_spelling": "haba",
        "informal_variants": [],
        "part_of_speech": "interjection",
        "definitions": ["exclamation of disbelief or protest"],
        "example_sentences": ["Haba, no be so."],
    },
    {
        "id": "kai",
        "standard_spelling": "kai",
        "informal_variants": [],
        "part_of_speech": "interjection",
        "definitions": ["exclamation of surprise or sympathy"],
        "example_sentences": ["Kai, wetin hapen?"],
    },
    {
        "id": "shuo",
        "standard_spelling": "shuo",
        "informal_variants": ["sho"],
        "part_of_speech": "interjection",
        "definitions": ["exclamation of surprise or emphasis"],
        "example_sentences": ["Shuo! Di fud sweet."],
    },
    {
        "id": "belleful",
        "standard_spelling": "belleful",
        "informal_variants": ["belle full", "beli-ful"],
        "part_of_speech": "adjective",
        "definitions": ["full (from eating); satisfied"],
        "example_sentences": ["I don belleful."],
    },
    {
        "id": "gbege",
        "standard_spelling": "gbege",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["trouble; serious problem"],
        "example_sentences": ["Gbege don start."],
    },
    {
        "id": "agbero",
        "standard_spelling": "agbero",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["motor-park tout / loader"],
        "example_sentences": ["Agbero de fo park."],
    },
    {
        "id": "molue",
        "standard_spelling": "molue",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["old Lagos mass-transit bus"],
        "example_sentences": ["I enta molue."],
    },
    {
        "id": "ofada",
        "standard_spelling": "ofada",
        "informal_variants": ["ofada-rice"],
        "part_of_speech": "noun",
        "definitions": ["local ofada rice (often with sauce)"],
        "example_sentences": ["I wan chop ofada."],
    },
    {
        "id": "efo",
        "standard_spelling": "efo",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["vegetable leaf soup / stew"],
        "example_sentences": ["Mama kuk efo."],
    },
    {
        "id": "ewedu",
        "standard_spelling": "ewedu",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["ewedu (jute-leaf soup)"],
        "example_sentences": ["Ewedu wit amala."],
    },
    {
        "id": "banga",
        "standard_spelling": "banga",
        "informal_variants": ["banga-soup"],
        "part_of_speech": "noun",
        "definitions": ["palm-nut soup"],
        "example_sentences": ["Banga soup sweet."],
    },
    {
        "id": "gala",
        "standard_spelling": "gala",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["sausage roll snack (brand-generic use)"],
        "example_sentences": ["Buy gala fo mi."],
    },
    {
        "id": "puff-puff",
        "standard_spelling": "puff-puff",
        "informal_variants": ["puff puff", "puffpuff"],
        "part_of_speech": "noun",
        "definitions": ["fried dough snack"],
        "example_sentences": ["I wan puff-puff."],
    },
    {
        "id": "eba",
        "standard_spelling": "eba",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["garri meal (eba)"],
        "example_sentences": ["I chop eba."],
    },
    {
        "id": "fufu",
        "standard_spelling": "fufu",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["pounded starch swallow"],
        "example_sentences": ["Fufu wit soup."],
    },
    {
        "id": "amala",
        "standard_spelling": "amala",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["yam-flour swallow"],
        "example_sentences": ["Amala wit ewedu."],
    },
    {
        "id": "gari",
        "standard_spelling": "gari",
        "informal_variants": ["garri"],
        "part_of_speech": "noun",
        "definitions": ["cassava flakes / garri"],
        "example_sentences": ["Soak gari."],
    },
    {
        "id": "ponmo",
        "standard_spelling": "ponmo",
        "informal_variants": ["pomo", "kpomo"],
        "part_of_speech": "noun",
        "definitions": ["cow skin (food)"],
        "example_sentences": ["Put ponmo fo soup."],
    },
    {
        "id": "zobo",
        "standard_spelling": "zobo",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["hibiscus drink"],
        "example_sentences": ["I wan drink zobo."],
    },
    {
        "id": "gen",
        "standard_spelling": "gen",
        "informal_variants": ["generator"],
        "part_of_speech": "noun",
        "definitions": ["generator (colloquial)"],
        "example_sentences": ["Put on di gen."],
    },
    {
        "id": "owambe",
        "standard_spelling": "owambe",
        "informal_variants": ["owambe-party"],
        "part_of_speech": "noun",
        "definitions": ["lavish party / celebration"],
        "example_sentences": ["Dem go owambe."],
    },
]


def main() -> int:
    entries = json.loads(DICT.read_text(encoding="utf-8"))
    by_id = {e["id"] for e in entries}
    added = 0
    for e in NEW:
        if e["id"] in by_id:
            print(f"skip existing id: {e['id']}", file=sys.stderr)
            continue
        std = e["standard_spelling"]
        e["informal_variants"] = [
            v for v in e.get("informal_variants", []) if v.casefold() != std.casefold()
        ]
        entries.append(e)
        by_id.add(e["id"])
        added += 1
    DICT.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added {added} entries; total now {len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
