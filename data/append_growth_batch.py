#!/usr/bin/env python3
"""Append lexicon-growth entries to dictionary.json without wiping enrichments."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\boija\OneDrive - UMass Lowell") / "'26Hussell shit" / "Pidgin Writng system"
DICT = ROOT / "data" / "dictionary.json"

# Keep in sync with build_seed.py growth batch (2026-09-27).
NEW = [
    {
        "id": "wey",
        "standard_spelling": "wey",
        "informal_variants": ["who", "which", "that"],
        "part_of_speech": "pronoun",
        "definitions": ["who; which; that (relativizer)"],
        "example_sentences": ["Di man wey kom yestade."],
    },
    {
        "id": "hia",
        "standard_spelling": "hia",
        "informal_variants": ["here"],
        "part_of_speech": "adverb",
        "definitions": ["here"],
        "example_sentences": ["Kom hia nau."],
    },
    {
        "id": "dea",
        "standard_spelling": "dea",
        "informal_variants": ["there"],
        "part_of_speech": "adverb",
        "definitions": ["there"],
        "example_sentences": ["Put di buk dea."],
    },
    {
        "id": "fone",
        "standard_spelling": "fone",
        "informal_variants": ["phone", "telephone"],
        "part_of_speech": "noun",
        "definitions": ["phone; telephone"],
        "example_sentences": ["Kari di fone."],
    },
    {
        "id": "wota",
        "standard_spelling": "wota",
        "informal_variants": ["water"],
        "part_of_speech": "noun",
        "definitions": ["water"],
        "example_sentences": ["Bring wota kom."],
    },
    {
        "id": "rais",
        "standard_spelling": "rais",
        "informal_variants": ["rice"],
        "part_of_speech": "noun",
        "definitions": ["rice"],
        "example_sentences": ["I wan chop rais."],
    },
    {
        "id": "ren",
        "standard_spelling": "ren",
        "informal_variants": ["rain"],
        "part_of_speech": "noun",
        "definitions": ["rain"],
        "example_sentences": ["Ren de fol."],
    },
    {
        "id": "bodi",
        "standard_spelling": "bodi",
        "informal_variants": ["body"],
        "part_of_speech": "noun",
        "definitions": ["body"],
        "example_sentences": ["Mai bodi de pein."],
    },
    {
        "id": "nos",
        "standard_spelling": "nos",
        "informal_variants": ["nose"],
        "part_of_speech": "noun",
        "definitions": ["nose"],
        "example_sentences": ["Im nos de run."],
    },
    {
        "id": "mout",
        "standard_spelling": "mout",
        "informal_variants": ["mouth"],
        "part_of_speech": "noun",
        "definitions": ["mouth"],
        "example_sentences": ["Lok yu mout."],
    },
    {
        "id": "drink",
        "standard_spelling": "drink",
        "informal_variants": [],
        "part_of_speech": "verb",
        "definitions": ["to drink"],
        "example_sentences": ["I wan drink wota."],
    },
    {
        "id": "ples",
        "standard_spelling": "ples",
        "informal_variants": ["place"],
        "part_of_speech": "noun",
        "definitions": ["place"],
        "example_sentences": ["Dis ples fine."],
    },
    {
        "id": "outsai",
        "standard_spelling": "outsai",
        "informal_variants": ["outside", "out"],
        "part_of_speech": "adverb",
        "definitions": ["outside"],
        "example_sentences": ["Go outsai."],
    },
    {
        "id": "klin",
        "standard_spelling": "klin",
        "informal_variants": ["clean"],
        "part_of_speech": "adjective",
        "definitions": ["clean; also used as verb “to clean”"],
        "example_sentences": ["Di haus klin.", "Klin di rum."],
    },
    {
        "id": "shaut",
        "standard_spelling": "shaut",
        "informal_variants": ["shout"],
        "part_of_speech": "verb",
        "definitions": ["to shout"],
        "example_sentences": ["No shaut fo hia."],
    },
    {
        "id": "hapen",
        "standard_spelling": "hapen",
        "informal_variants": ["happen"],
        "part_of_speech": "verb",
        "definitions": ["to happen"],
        "example_sentences": ["Wetin hapen?"],
    },
    {
        "id": "fa",
        "standard_spelling": "fa",
        "informal_variants": ["far"],
        "part_of_speech": "adjective",
        "definitions": ["far"],
        "example_sentences": ["Di ples fa."],
    },
    {
        "id": "yong",
        "standard_spelling": "yong",
        "informal_variants": ["young"],
        "part_of_speech": "adjective",
        "definitions": ["young"],
        "example_sentences": ["Yong man de waka."],
    },
    {
        "id": "niu",
        "standard_spelling": "niu",
        "informal_variants": ["new"],
        "part_of_speech": "adjective",
        "definitions": ["new"],
        "example_sentences": ["I get niu buk."],
    },
    {
        "id": "tii",
        "standard_spelling": "tii",
        "informal_variants": ["tea"],
        "part_of_speech": "noun",
        "definitions": ["tea"],
        "example_sentences": ["I wan tii."],
    },
    {
        "id": "kofe",
        "standard_spelling": "kofe",
        "informal_variants": ["coffee"],
        "part_of_speech": "noun",
        "definitions": ["coffee"],
        "example_sentences": ["I wan kofe."],
    },
    {
        "id": "shuz",
        "standard_spelling": "shuz",
        "informal_variants": ["shoe", "shoes"],
        "part_of_speech": "noun",
        "definitions": ["shoe; shoes"],
        "example_sentences": ["Put yu shuz."],
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
