#!/usr/bin/env python3
"""Append lexicon-growth batch 6 to dictionary.json without wiping enrichments."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICT = ROOT / "data" / "dictionary.json"

# Lexicon growth batch 6 — slang, address terms, food (2026-09-27). No IME/Keyman refresh.
NEW = [
    {
        "id": "ajepako",
        "standard_spelling": "ajepako",
        "informal_variants": ["aje pako"],
        "part_of_speech": "noun",
        "definitions": ["person from a rough / street background (contrast ajebutter)"],
        "example_sentences": ["Im na ajepako."],
    },
    {
        "id": "kpali",
        "standard_spelling": "kpali",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["trouble; serious problem (slang)"],
        "example_sentences": ["Kpali don enter."],
    },
    {
        "id": "area-boy",
        "standard_spelling": "area boy",
        "informal_variants": ["areaboy", "area-boys"],
        "part_of_speech": "noun",
        "definitions": ["street tout / neighborhood hustler"],
        "example_sentences": ["Area boy de fo junction."],
    },
    {
        "id": "one-chance",
        "standard_spelling": "one chance",
        "informal_variants": ["onechance", "one-chance"],
        "part_of_speech": "noun",
        "definitions": ["shared informal taxi / ride (Lagos slang)"],
        "example_sentences": ["I tek one chance go wok."],
    },
    {
        "id": "no-dulling",
        "standard_spelling": "no dulling",
        "informal_variants": ["nodulling", "no-dulling"],
        "part_of_speech": "phrase",
        "definitions": ["don't mess around; stay sharp / serious"],
        "example_sentences": ["No dulling for this mata."],
    },
    {
        "id": "sabi-book",
        "standard_spelling": "sabi book",
        "informal_variants": ["sabibook", "sabi-book"],
        "part_of_speech": "noun",
        "definitions": ["book-smart person; academic type"],
        "example_sentences": ["Im na sabi book."],
    },
    {
        "id": "shine-your-eye",
        "standard_spelling": "shine your eye",
        "informal_variants": ["shine-your-eye", "shine ya eye"],
        "part_of_speech": "phrase",
        "definitions": ["be alert; watch out; wise up"],
        "example_sentences": ["Shine your eye fo market."],
    },
    {
        "id": "soft-life",
        "standard_spelling": "soft life",
        "informal_variants": ["softlife", "soft-life"],
        "part_of_speech": "noun",
        "definitions": ["comfortable / easy living"],
        "example_sentences": ["Im de live soft life."],
    },
    {
        "id": "hard-life",
        "standard_spelling": "hard life",
        "informal_variants": ["hardlife", "hard-life"],
        "part_of_speech": "noun",
        "definitions": ["difficult living; struggle"],
        "example_sentences": ["Hard life no easy."],
    },
    {
        "id": "my-guy",
        "standard_spelling": "my guy",
        "informal_variants": ["myguy", "my-guy"],
        "part_of_speech": "phrase",
        "definitions": ["friendly address; mate"],
        "example_sentences": ["How far, my guy?"],
    },
    {
        "id": "bros",
        "standard_spelling": "bros",
        "informal_variants": ["bro", "brother"],
        "part_of_speech": "noun",
        "definitions": ["brother; male peer (address)"],
        "example_sentences": ["Bros, abeg help mi."],
    },
    {
        "id": "padi",
        "standard_spelling": "padi",
        "informal_variants": ["paddy", "padie"],
        "part_of_speech": "noun",
        "definitions": ["friend; buddy"],
        "example_sentences": ["Im na mai padi."],
    },
    {
        "id": "omo",
        "standard_spelling": "omo",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["child; person (address / slang)"],
        "example_sentences": ["Omo, yu try."],
    },
    {
        "id": "alaye",
        "standard_spelling": "alaye",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["street-smart person; also used as address"],
        "example_sentences": ["Alaye, wetin de happen?"],
    },
    {
        "id": "shey",
        "standard_spelling": "shey",
        "informal_variants": ["sey"],
        "part_of_speech": "particle",
        "definitions": ["tag / confirmation particle (right; isn't it)"],
        "example_sentences": ["Shey yu de go?"],
    },
    {
        "id": "pepper-soup",
        "standard_spelling": "pepper soup",
        "informal_variants": ["peppersoup", "pepper-soup"],
        "part_of_speech": "noun",
        "definitions": ["spicy broth (often fish or meat)"],
        "example_sentences": ["I wan pepper soup."],
    },
    {
        "id": "isi-ewu",
        "standard_spelling": "isi ewu",
        "informal_variants": ["isiewu", "isi-ewu"],
        "part_of_speech": "noun",
        "definitions": ["spicy goat-head dish"],
        "example_sentences": ["Dem chop isi ewu."],
    },
    {
        "id": "asun",
        "standard_spelling": "asun",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["spicy grilled goat meat"],
        "example_sentences": ["Buy asun fo mi."],
    },
    {
        "id": "nkwobi",
        "standard_spelling": "nkwobi",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["spicy cow-foot dish"],
        "example_sentences": ["Nkwobi sweet."],
    },
    {
        "id": "kilishi",
        "standard_spelling": "kilishi",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["spiced dried meat (jerky-style)"],
        "example_sentences": ["I buy kilishi."],
    },
    {
        "id": "agege",
        "standard_spelling": "agege",
        "informal_variants": ["agege-bread"],
        "part_of_speech": "noun",
        "definitions": ["Agege-style soft bread"],
        "example_sentences": ["Agege bread wit stew."],
    },
    {
        "id": "shawarma",
        "standard_spelling": "shawarma",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["shawarma wrap (street food)"],
        "example_sentences": ["I wan shawarma."],
    },
    {
        "id": "indomie",
        "standard_spelling": "indomie",
        "informal_variants": ["indo"],
        "part_of_speech": "noun",
        "definitions": ["instant noodles (genericized brand use)"],
        "example_sentences": ["Kuk indomie fo mi."],
    },
    {
        "id": "akpu",
        "standard_spelling": "akpu",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["fermented cassava swallow"],
        "example_sentences": ["Akpu wit soup."],
    },
    {
        "id": "okpa",
        "standard_spelling": "okpa",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["bambara-nut pudding"],
        "example_sentences": ["I chop okpa."],
    },
    {
        "id": "kpekere",
        "standard_spelling": "kpekere",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["fried plantain chips"],
        "example_sentences": ["Buy kpekere."],
    },
    {
        "id": "plantain",
        "standard_spelling": "plantain",
        "informal_variants": ["plaintain"],
        "part_of_speech": "noun",
        "definitions": ["plantain"],
        "example_sentences": ["Fry di plantain."],
    },
    {
        "id": "beans",
        "standard_spelling": "beans",
        "informal_variants": ["binch"],
        "part_of_speech": "noun",
        "definitions": ["beans (food)"],
        "example_sentences": ["Beans wit dodo."],
    },
    {
        "id": "stew",
        "standard_spelling": "stew",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["tomato-based stew"],
        "example_sentences": ["Put stew fo rais."],
    },
    {
        "id": "palm-wine",
        "standard_spelling": "palm wine",
        "informal_variants": ["palmwine", "palm-wine"],
        "part_of_speech": "noun",
        "definitions": ["palm wine"],
        "example_sentences": ["Dem drink palm wine."],
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
