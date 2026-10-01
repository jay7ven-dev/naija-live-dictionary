#!/usr/bin/env python3
"""Append lexicon-growth batch 7 to dictionary.json without wiping enrichments."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICT = ROOT / "data" / "dictionary.json"

# Lexicon growth batch 7 — slang, address, staples (2026-10-01). No IME/Keyman refresh.
NEW = [
    {
        "id": "vibe",
        "standard_spelling": "vibe",
        "informal_variants": ["vibes"],
        "part_of_speech": "noun",
        "definitions": ["mood; atmosphere; good energy"],
        "example_sentences": ["Di vibe sweet."],
    },
    {
        "id": "razz",
        "standard_spelling": "razz",
        "informal_variants": [],
        "part_of_speech": "verb",
        "definitions": ["to tease; mock; play with"],
        "example_sentences": ["No razz mi."],
    },
    {
        "id": "maga",
        "standard_spelling": "maga",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["dupe; scam victim (slang)"],
        "example_sentences": ["Dem find maga."],
    },
    {
        "id": "yahoo",
        "standard_spelling": "yahoo",
        "informal_variants": ["yahoo-yahoo"],
        "part_of_speech": "noun",
        "definitions": ["internet fraud (slang); fraudster scene"],
        "example_sentences": ["E no de do yahoo."],
    },
    {
        "id": "level",
        "standard_spelling": "level",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["status; standard; situation"],
        "example_sentences": ["Wetin be di level?"],
    },
    {
        "id": "correct",
        "standard_spelling": "correct",
        "informal_variants": [],
        "part_of_speech": "adjective",
        "definitions": ["proper; solid; reliable (slang praise)"],
        "example_sentences": ["Di guy correct."],
    },
    {
        "id": "hammer",
        "standard_spelling": "hammer",
        "informal_variants": [],
        "part_of_speech": "verb",
        "definitions": ["to succeed big; cash out (slang)"],
        "example_sentences": ["E don hammer."],
    },
    {
        "id": "gbana",
        "standard_spelling": "gbana",
        "informal_variants": [],
        "part_of_speech": "verb",
        "definitions": ["to snatch; steal by force (slang)"],
        "example_sentences": ["Dem wan gbana di fone."],
    },
    {
        "id": "bend-down",
        "standard_spelling": "bend down",
        "informal_variants": ["bend-down", "bendown"],
        "part_of_speech": "phrase",
        "definitions": ["cheap roadside goods market"],
        "example_sentences": ["I buy am fo bend down."],
    },
    {
        "id": "allowee",
        "standard_spelling": "allowee",
        "informal_variants": ["allowance"],
        "part_of_speech": "noun",
        "definitions": ["pocket money; allowance"],
        "example_sentences": ["Mai allowee don finish."],
    },
    {
        "id": "madam",
        "standard_spelling": "madam",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["woman of status; polite female address"],
        "example_sentences": ["Madam, abeg."],
    },
    {
        "id": "chief",
        "standard_spelling": "chief",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["chief; also playful male address"],
        "example_sentences": ["Chief, how far?"],
    },
    {
        "id": "sis",
        "standard_spelling": "sis",
        "informal_variants": ["sister"],
        "part_of_speech": "noun",
        "definitions": ["sister; female peer (address)"],
        "example_sentences": ["Sis, yu try."],
    },
    {
        "id": "aunty",
        "standard_spelling": "aunty",
        "informal_variants": ["auntie"],
        "part_of_speech": "noun",
        "definitions": ["aunt; respectful address for older woman"],
        "example_sentences": ["Aunty, good morning."],
    },
    {
        "id": "uncle",
        "standard_spelling": "uncle",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["uncle; respectful address for older man"],
        "example_sentences": ["Uncle, abeg help mi."],
    },
    {
        "id": "babe",
        "standard_spelling": "babe",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["attractive woman; informal address"],
        "example_sentences": ["Babe, how you dey?"],
    },
    {
        "id": "fine-boy",
        "standard_spelling": "fine boy",
        "informal_variants": ["fineboy", "fine-boy"],
        "part_of_speech": "noun",
        "definitions": ["handsome young man"],
        "example_sentences": ["Im na fine boy."],
    },
    {
        "id": "fine-girl",
        "standard_spelling": "fine girl",
        "informal_variants": ["finegirl", "fine-girl"],
        "part_of_speech": "noun",
        "definitions": ["beautiful young woman"],
        "example_sentences": ["Im na fine girl."],
    },
    {
        "id": "how-body",
        "standard_spelling": "how body",
        "informal_variants": ["howbody", "how-body"],
        "part_of_speech": "phrase",
        "definitions": ["how are you; how is health"],
        "example_sentences": ["How body?"],
    },
    {
        "id": "small-chop",
        "standard_spelling": "small chop",
        "informal_variants": ["smallchop", "small-chop"],
        "part_of_speech": "noun",
        "definitions": ["finger food; party snacks"],
        "example_sentences": ["Small chop don ready."],
    },
    {
        "id": "ukwa",
        "standard_spelling": "ukwa",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["breadfruit (food)"],
        "example_sentences": ["I chop ukwa."],
    },
    {
        "id": "bushmeat",
        "standard_spelling": "bushmeat",
        "informal_variants": ["bush-meat", "bush meat"],
        "part_of_speech": "noun",
        "definitions": ["wild game meat"],
        "example_sentences": ["Dem sell bushmeat."],
    },
    {
        "id": "jazz",
        "standard_spelling": "jazz",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["charm; juju; spiritual concoction (slang)"],
        "example_sentences": ["E use jazz."],
    },
    {
        "id": "scode",
        "standard_spelling": "scode",
        "informal_variants": ["s-code"],
        "part_of_speech": "noun",
        "definitions": ["street code; unspoken street rules"],
        "example_sentences": ["Sabi di scode."],
    },
    {
        "id": "carry-go",
        "standard_spelling": "carry go",
        "informal_variants": ["carrygo", "carry-go"],
        "part_of_speech": "phrase",
        "definitions": ["take away; pack and leave; to-go"],
        "example_sentences": ["Make e carry go."],
    },
    {
        "id": "toast",
        "standard_spelling": "toast",
        "informal_variants": [],
        "part_of_speech": "verb",
        "definitions": ["to praise; hype; celebrate someone (slang)"],
        "example_sentences": ["Dem de toast am."],
    },
    {
        "id": "street",
        "standard_spelling": "street",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["the street; street life / hustle"],
        "example_sentences": ["Street no easy."],
    },
    {
        "id": "chairman",
        "standard_spelling": "chairman",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["chairman; also playful respectful address"],
        "example_sentences": ["Chairman, abeg."],
    },
    {
        "id": "balangu",
        "standard_spelling": "balangu",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["grilled spiced meat (northern style)"],
        "example_sentences": ["I wan balangu."],
    },
    {
        "id": "burukutu",
        "standard_spelling": "burukutu",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["local fermented cereal drink"],
        "example_sentences": ["Dem drink burukutu."],
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
