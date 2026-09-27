#!/usr/bin/env python3
"""Merge growth near-duplicates into seed headwords; append growth batch 3."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICT = ROOT / "data" / "dictionary.json"
MAPPINGS = ROOT / "data" / "variant_mappings.json"

# Drop growth ids → keep seed ids; merge variants/examples onto keep.
MERGE = {
    "wota": "wata",
    "frend": "fren",
    "bele": "belle",
    "nos": "noz",
    "mout": "maut",
}

BATCH3 = [
    {
        "id": "aftanun",
        "standard_spelling": "aftanun",
        "informal_variants": ["afternoon", "aftanoon"],
        "part_of_speech": "noun",
        "definitions": ["afternoon"],
        "example_sentences": ["Si yu aftanun."],
    },
    {
        "id": "ivnin",
        "standard_spelling": "ivnin",
        "informal_variants": ["evening", "evenin"],
        "part_of_speech": "noun",
        "definitions": ["evening"],
        "example_sentences": ["Gud ivnin."],
    },
    {
        "id": "minit",
        "standard_spelling": "minit",
        "informal_variants": ["minute", "minutes"],
        "part_of_speech": "noun",
        "definitions": ["minute"],
        "example_sentences": ["Weit wan minit."],
    },
    {
        "id": "san",
        "standard_spelling": "san",
        "informal_variants": ["sun"],
        "part_of_speech": "noun",
        "definitions": ["sun"],
        "example_sentences": ["San de hot."],
    },
    {
        "id": "teja",
        "standard_spelling": "teja",
        "informal_variants": ["teacher"],
        "part_of_speech": "noun",
        "definitions": ["teacher"],
        "example_sentences": ["Di teja de tish."],
    },
    {
        "id": "studet",
        "standard_spelling": "studet",
        "informal_variants": ["student"],
        "part_of_speech": "noun",
        "definitions": ["student"],
        "example_sentences": ["Im na gud studet."],
    },
    {
        "id": "driva",
        "standard_spelling": "driva",
        "informal_variants": ["driver"],
        "part_of_speech": "noun",
        "definitions": ["driver"],
        "example_sentences": ["Di driva de wait."],
    },
    {
        "id": "soldia",
        "standard_spelling": "soldia",
        "informal_variants": ["soldier"],
        "part_of_speech": "noun",
        "definitions": ["soldier"],
        "example_sentences": ["Soldia de fo gate."],
    },
    {
        "id": "mit",
        "standard_spelling": "mit",
        "informal_variants": ["meat"],
        "part_of_speech": "noun",
        "definitions": ["meat"],
        "example_sentences": ["I wan chop mit."],
    },
    {
        "id": "had",
        "standard_spelling": "had",
        "informal_variants": ["hard"],
        "part_of_speech": "adjective",
        "definitions": ["hard; difficult"],
        "example_sentences": ["Di wok had."],
    },
    {
        "id": "soft",
        "standard_spelling": "soft",
        "informal_variants": [],
        "part_of_speech": "adjective",
        "definitions": ["soft"],
        "example_sentences": ["Di bed soft."],
    },
    {
        "id": "kwaiet",
        "standard_spelling": "kwaiet",
        "informal_variants": ["quiet"],
        "part_of_speech": "adjective",
        "definitions": ["quiet"],
        "example_sentences": ["Mek di ples kwaiet."],
    },
    {
        "id": "sawa",
        "standard_spelling": "sawa",
        "informal_variants": ["sour"],
        "part_of_speech": "adjective",
        "definitions": ["sour"],
        "example_sentences": ["Di orenj sawa."],
    },
    {
        "id": "smel",
        "standard_spelling": "smel",
        "informal_variants": ["smell"],
        "part_of_speech": "verb",
        "definitions": ["to smell; a smell"],
        "example_sentences": ["Smel di fud."],
    },
    {
        "id": "noiz",
        "standard_spelling": "noiz",
        "informal_variants": ["noise"],
        "part_of_speech": "noun",
        "definitions": ["noise"],
        "example_sentences": ["Tu noiz fo hia."],
    },
    {
        "id": "jomp",
        "standard_spelling": "jomp",
        "informal_variants": ["jump"],
        "part_of_speech": "verb",
        "definitions": ["to jump"],
        "example_sentences": ["Pikin de jomp."],
    },
    {
        "id": "smail",
        "standard_spelling": "smail",
        "informal_variants": ["smile"],
        "part_of_speech": "verb",
        "definitions": ["to smile"],
        "example_sentences": ["Im de smail."],
    },
    {
        "id": "boro",
        "standard_spelling": "boro",
        "informal_variants": ["borrow"],
        "part_of_speech": "verb",
        "definitions": ["to borrow"],
        "example_sentences": ["I wan boro moni."],
    },
    {
        "id": "lok",
        "standard_spelling": "lok",
        "informal_variants": ["lock"],
        "part_of_speech": "verb",
        "definitions": ["to lock"],
        "example_sentences": ["Lok di do."],
    },
    {
        "id": "bring",
        "standard_spelling": "bring",
        "informal_variants": [],
        "part_of_speech": "verb",
        "definitions": ["to bring"],
        "example_sentences": ["Bring wata kom."],
    },
    {
        "id": "taun",
        "standard_spelling": "taun",
        "informal_variants": ["town"],
        "part_of_speech": "noun",
        "definitions": ["town"],
        "example_sentences": ["I de go taun."],
    },
    {
        "id": "siti",
        "standard_spelling": "siti",
        "informal_variants": ["city"],
        "part_of_speech": "noun",
        "definitions": ["city"],
        "example_sentences": ["Lagos na big siti."],
    },
    {
        "id": "kontri",
        "standard_spelling": "kontri",
        "informal_variants": ["country"],
        "part_of_speech": "noun",
        "definitions": ["country"],
        "example_sentences": ["Mai kontri na Naija."],
    },
    {
        "id": "prais",
        "standard_spelling": "prais",
        "informal_variants": ["price"],
        "part_of_speech": "noun",
        "definitions": ["price"],
        "example_sentences": ["Hau mush prais?"],
    },
    {
        "id": "biko",
        "standard_spelling": "biko",
        "informal_variants": [],
        "part_of_speech": "interjection",
        "definitions": ["please (Igbo-origin polite particle)"],
        "example_sentences": ["Biko help mi."],
    },
    {
        "id": "fiva",
        "standard_spelling": "fiva",
        "informal_variants": ["fever"],
        "part_of_speech": "noun",
        "definitions": ["fever"],
        "example_sentences": ["Im get fiva."],
    },
    {
        "id": "medisin",
        "standard_spelling": "medisin",
        "informal_variants": ["medicine", "medin"],
        "part_of_speech": "noun",
        "definitions": ["medicine"],
        "example_sentences": ["Tek yu medisin."],
    },
]


def merge_entry(keep: dict, drop: dict) -> None:
    vars_ = list(keep.get("informal_variants") or [])
    seen = {v.casefold() for v in vars_}
    std = keep["standard_spelling"].casefold()
    for v in drop.get("informal_variants") or []:
        if v.casefold() == std or v.casefold() in seen:
            continue
        vars_.append(v)
        seen.add(v.casefold())
    # keep dropped standard as informal if different
    ds = drop["standard_spelling"]
    if ds.casefold() != std and ds.casefold() not in seen:
        vars_.append(ds)
        seen.add(ds.casefold())
    keep["informal_variants"] = vars_
    ex = list(keep.get("example_sentences") or [])
    ex_seen = {e.casefold() for e in ex}
    for e in drop.get("example_sentences") or []:
        if e.casefold() not in ex_seen:
            ex.append(e)
            ex_seen.add(e.casefold())
    keep["example_sentences"] = ex
    # prefer existing notes/pron on keep; copy pron if missing
    if not keep.get("pronunciation") and drop.get("pronunciation"):
        keep["pronunciation"] = drop["pronunciation"]
    if not keep.get("notes") and drop.get("notes"):
        keep["notes"] = drop["notes"]


def main() -> int:
    entries = json.loads(DICT.read_text(encoding="utf-8"))
    by_id = {e["id"]: e for e in entries}

    removed = 0
    for drop_id, keep_id in MERGE.items():
        if drop_id not in by_id or keep_id not in by_id:
            print(f"skip merge {drop_id}->{keep_id} (missing)")
            continue
        merge_entry(by_id[keep_id], by_id[drop_id])
        del by_id[drop_id]
        removed += 1
        print(f"merged {drop_id} -> {keep_id}")

    entries = list(by_id.values())

    # retarget mappings
    mdata = json.loads(MAPPINGS.read_text(encoding="utf-8"))
    remapped = 0
    for row in mdata["mappings"]:
        eid = row["entry_id"]
        if eid in MERGE:
            row["entry_id"] = MERGE[eid]
            remapped += 1
            note = row.get("note") or ""
            if "retarget" not in note:
                row["note"] = (note + f" [retarget {eid}->{MERGE[eid]}]").strip()
    # dedupe mapping keys
    seen_k = set()
    new_maps = []
    for row in mdata["mappings"]:
        key = (row["variant"].casefold(), row["entry_id"])
        if key in seen_k:
            continue
        seen_k.add(key)
        new_maps.append(row)
    mdata["mappings"] = new_maps
    MAPPINGS.write_text(json.dumps(mdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"retargeted {remapped} mappings; total {len(new_maps)}")

    # append batch 3
    existing = {e["id"] for e in entries}
    added = 0
    for e in BATCH3:
        if e["id"] in existing:
            print(f"skip existing {e['id']}")
            continue
        std = e["standard_spelling"]
        e["informal_variants"] = [v for v in e.get("informal_variants", []) if v != std]
        entries.append(e)
        existing.add(e["id"])
        added += 1

    DICT.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"removed {removed} dupes; added {added}; total {len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
