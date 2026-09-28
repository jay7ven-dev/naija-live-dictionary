#!/usr/bin/env python3
"""Append lexicon-growth batch 4 to dictionary.json without wiping enrichments."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICT = ROOT / "data" / "dictionary.json"

# Lexicon growth batch 4 — discourse, transport, food, daily digital (2026-09-27).
NEW = [
    {
        "id": "nah",
        "standard_spelling": "nah",
        "informal_variants": ["naah", "naa"],
        "part_of_speech": "particle",
        "definitions": ["agreement / soft yeah; okay"],
        "example_sentences": ["Nah, I de kom."],
    },
    {
        "id": "ehen",
        "standard_spelling": "ehen",
        "informal_variants": ["Ehen", "ehhen"],
        "part_of_speech": "interjection",
        "definitions": ["discourse particle (recognition, interest, go-on)"],
        "example_sentences": ["Ehen, wetin hapen?"],
    },
    {
        "id": "mtchew",
        "standard_spelling": "mtchew",
        "informal_variants": ["mchew"],
        "part_of_speech": "interjection",
        "definitions": ["suck-teeth; disapproval or dismissal"],
        "example_sentences": ["Mtchew, leave mi."],
    },
    {
        "id": "yawa",
        "standard_spelling": "yawa",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["trouble; serious problem"],
        "example_sentences": ["Yawa don gas."],
    },
    {
        "id": "komot",
        "standard_spelling": "komot",
        "informal_variants": ["commot", "comot", "come-out"],
        "part_of_speech": "verb",
        "definitions": ["to come out; leave; get out"],
        "example_sentences": ["Komot fo rod."],
    },
    {
        "id": "enta",
        "standard_spelling": "enta",
        "informal_variants": ["enter"],
        "part_of_speech": "verb",
        "definitions": ["to enter; go in"],
        "example_sentences": ["Enta di rum."],
    },
    {
        "id": "kolekt",
        "standard_spelling": "kolekt",
        "informal_variants": ["collect", "kolec"],
        "part_of_speech": "verb",
        "definitions": ["to collect; pick up"],
        "example_sentences": ["I go kolekt di moni."],
    },
    {
        "id": "tokunbo",
        "standard_spelling": "tokunbo",
        "informal_variants": ["tokumbo", "second-hand"],
        "part_of_speech": "adjective",
        "definitions": ["used; second-hand (esp. imported goods)"],
        "example_sentences": ["I buy tokunbo laptop."],
    },
    {
        "id": "oyibo",
        "standard_spelling": "oyibo",
        "informal_variants": ["oyinbo", "white-man"],
        "part_of_speech": "noun",
        "definitions": ["white person; foreigner; Western-style"],
        "example_sentences": ["Oyibo de fo hia."],
    },
    {
        "id": "jare",
        "standard_spelling": "jare",
        "informal_variants": ["jaree"],
        "part_of_speech": "particle",
        "definitions": ["emphatic / softener particle (please; indeed)"],
        "example_sentences": ["Abeg jare, help mi."],
    },
    {
        "id": "yarn",
        "standard_spelling": "yarn",
        "informal_variants": ["yan"],
        "part_of_speech": "verb",
        "definitions": ["to talk; chat; narrate"],
        "example_sentences": ["Make we yarn."],
    },
    {
        "id": "mumu",
        "standard_spelling": "mumu",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["fool; foolish person"],
        "example_sentences": ["No be mumu."],
    },
    {
        "id": "mugu",
        "standard_spelling": "mugu",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["dupe; gullible person (scam context)"],
        "example_sentences": ["Dem find mugu."],
    },
    {
        "id": "danfo",
        "standard_spelling": "danfo",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["yellow Lagos minibus"],
        "example_sentences": ["I enta danfo go wok."],
    },
    {
        "id": "okada",
        "standard_spelling": "okada",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["commercial motorcycle taxi"],
        "example_sentences": ["Tek okada go skul."],
    },
    {
        "id": "keke",
        "standard_spelling": "keke",
        "informal_variants": ["keke-napep"],
        "part_of_speech": "noun",
        "definitions": ["tricycle taxi"],
        "example_sentences": ["Keke de wait."],
    },
    {
        "id": "bole",
        "standard_spelling": "bole",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["roasted plantain (street food)"],
        "example_sentences": ["I wan chop bole."],
    },
    {
        "id": "suya",
        "standard_spelling": "suya",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["spiced grilled meat skewer"],
        "example_sentences": ["Buy suya fo mi."],
    },
    {
        "id": "jollof",
        "standard_spelling": "jollof",
        "informal_variants": ["jollof-rice"],
        "part_of_speech": "noun",
        "definitions": ["jollof rice"],
        "example_sentences": ["Di jollof sweet."],
    },
    {
        "id": "ogbono",
        "standard_spelling": "ogbono",
        "informal_variants": [],
        "part_of_speech": "noun",
        "definitions": ["ogbono (draw soup)"],
        "example_sentences": ["Mama kuk ogbono."],
    },
    {
        "id": "nepa",
        "standard_spelling": "nepa",
        "informal_variants": ["NEPA", "phcn"],
        "part_of_speech": "noun",
        "definitions": ["electricity supply / power authority (colloquial)"],
        "example_sentences": ["Nepa don kom."],
    },
    {
        "id": "airtime",
        "standard_spelling": "airtime",
        "informal_variants": ["recharge-card"],
        "part_of_speech": "noun",
        "definitions": ["mobile phone credit"],
        "example_sentences": ["I no get airtime."],
    },
    {
        "id": "small-small",
        "standard_spelling": "small-small",
        "informal_variants": ["small small"],
        "part_of_speech": "adverb",
        "definitions": ["gradually; little by little"],
        "example_sentences": ["Small-small we go rich."],
    },
    {
        "id": "now-now",
        "standard_spelling": "now-now",
        "informal_variants": ["now now", "nownow"],
        "part_of_speech": "adverb",
        "definitions": ["right away; immediately"],
        "example_sentences": ["I de kom now-now."],
    },
    {
        "id": "how-far",
        "standard_spelling": "how far",
        "informal_variants": ["howfar", "how-far"],
        "part_of_speech": "phrase",
        "definitions": ["greeting; how are you / what's up"],
        "example_sentences": ["How far, my guy?"],
    },
    {
        "id": "na-wa",
        "standard_spelling": "na wa",
        "informal_variants": ["nawa", "na-wa-o", "na wa o"],
        "part_of_speech": "interjection",
        "definitions": ["expression of surprise or exasperation"],
        "example_sentences": ["Na wa o!"],
    },
    {
        "id": "chai",
        "standard_spelling": "chai",
        "informal_variants": [],
        "part_of_speech": "interjection",
        "definitions": ["exclamation of surprise or empathy"],
        "example_sentences": ["Chai, wetin hapen?"],
    },
    {
        "id": "shebi",
        "standard_spelling": "shebi",
        "informal_variants": ["sebi"],
        "part_of_speech": "particle",
        "definitions": ["tag / confirmation particle (isn't it; right)"],
        "example_sentences": ["Shebi yu de go?"],
    },
    {
        "id": "ajebutter",
        "standard_spelling": "ajebutter",
        "informal_variants": ["aje butter", "ajebo"],
        "part_of_speech": "noun",
        "definitions": ["wealthy / soft-life person (slang)"],
        "example_sentences": ["Im na ajebutter."],
    },
    {
        "id": "pure-water",
        "standard_spelling": "pure water",
        "informal_variants": ["purewater", "sachet-water"],
        "part_of_speech": "noun",
        "definitions": ["sachet drinking water"],
        "example_sentences": ["Buy pure water."],
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
        e["informal_variants"] = [v for v in e.get("informal_variants", []) if v.casefold() != std.casefold()]
        entries.append(e)
        by_id.add(e["id"])
        added += 1
    DICT.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added {added} entries; total now {len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
