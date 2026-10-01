#!/usr/bin/env python3
"""Option A: phrase bank + usage notes + internal evidence counts (not public UI)."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICT = ROOT / "data" / "dictionary.json"
EVIDENCE = ROOT / "data" / "evidence_counts.json"
SOURCES = ROOT / "data" / "corpus" / "sources.json"
MAPPINGS = ROOT / "data" / "variant_mappings.json"

# ponytail: usage explanations live in notes — no schema field until UI needs it
USAGE = "Usage: "

PHRASES: list[dict] = [
    {
        "id": "abeg-mek",
        "standard_spelling": "abeg mek",
        "informal_variants": ["abeg make", "abegi make"],
        "part_of_speech": "phrase",
        "definitions": ["please let…; soft request frame"],
        "example_sentences": ["Abeg mek yu help mi."],
        "notes": USAGE
        + "Opens a polite request or plea (not a literal 'beg make'). Often softens a following clause.",
    },
    {
        "id": "e-choke",
        "standard_spelling": "e choke",
        "informal_variants": ["e choke!", "echoke"],
        "part_of_speech": "phrase",
        "definitions": ["that's intense; wow (exclamation of impact)"],
        "example_sentences": ["Di music sweet — e choke!"],
        "notes": USAGE
        + "Praise or shock reaction; not literal choking. Informal/youth register.",
    },
    {
        "id": "wetin-de-happen",
        "standard_spelling": "wetin de happen",
        "informal_variants": ["wetin dey happen", "what's happening", "wetin dey happen?"],
        "part_of_speech": "phrase",
        "definitions": ["what's going on; what's happening"],
        "example_sentences": ["Wetin de happen hia?"],
        "notes": USAGE
        + "Asks for the situation or news, not a formal event schedule. Related to shorter 'wetin de'.",
    },
    {
        "id": "na-so",
        "standard_spelling": "na so",
        "informal_variants": ["na so!", "that's how"],
        "part_of_speech": "phrase",
        "definitions": ["that's how it is; exactly; agreement"],
        "example_sentences": ["Na so e bi."],
        "notes": USAGE
        + "Confirms agreement or resigns to how things are ('that's the way').",
    },
    {
        "id": "abeg-nau",
        "standard_spelling": "abeg nau",
        "informal_variants": ["abeg now", "abeg nao"],
        "part_of_speech": "phrase",
        "definitions": ["come on; please now (emphatic plea or mild protest)"],
        "example_sentences": ["Abeg nau, no vex."],
        "notes": USAGE
        + "Emphatic 'please/come on' — can soften or push back depending on tone.",
    },
    {
        "id": "wetin-be-dis",
        "standard_spelling": "wetin be dis",
        "informal_variants": ["weytin be dis", "wetin be this", "what is this"],
        "part_of_speech": "phrase",
        "definitions": ["what is this; what's going on here (surprise or complaint)"],
        "example_sentences": ["Wetin be dis?"],
        "notes": USAGE
        + "Often rhetorical surprise or mild complaint, not a neutral information question.",
    },
    {
        "id": "kari-go",
        "standard_spelling": "kari go",
        "informal_variants": ["carry go", "carry-go"],
        "part_of_speech": "phrase",
        "definitions": ["take (it) away; go ahead and take"],
        "example_sentences": ["Kari go — I no nid am."],
        "notes": USAGE
        + "Directive to take something away or proceed with taking; not 'carry' as lift only.",
    },
    {
        "id": "i-de-kom",
        "standard_spelling": "I de kom",
        "informal_variants": ["I dey come", "i dey come", "I'm coming"],
        "part_of_speech": "phrase",
        "definitions": ["I'm on my way; I'll be right there"],
        "example_sentences": ["Wét — I de kom."],
        "notes": USAGE
        + "Often means 'I'm coming soon / on my way', not always literal motion right now.",
    },
    {
        "id": "i-no-fit",
        "standard_spelling": "I no fit",
        "informal_variants": ["i no fit", "I can't", "i cannot"],
        "part_of_speech": "phrase",
        "definitions": ["I can't; I'm not able"],
        "example_sentences": ["I no fit kom tumoro."],
        "notes": USAGE
        + "Ability refusal: can't / won't be able — not 'I do not fit' physically.",
    },
    {
        "id": "i-no-sabi",
        "standard_spelling": "I no sabi",
        "informal_variants": ["i no sabi", "I don't know", "i don't know"],
        "part_of_speech": "phrase",
        "definitions": ["I don't know; I don't understand"],
        "example_sentences": ["I no sabi wetin e mean."],
        "notes": USAGE
        + "Denial of knowledge/understanding; common discourse response.",
    },
    {
        "id": "no-vex",
        "standard_spelling": "no vex",
        "informal_variants": ["no vex!", "don't vex", "don't be angry"],
        "part_of_speech": "phrase",
        "definitions": ["don't be angry; sorry; calm down"],
        "example_sentences": ["No vex — I go fix am."],
        "notes": USAGE
        + "Apology / softener asking someone not to be upset; social repair, not medical 'vexation'.",
    },
]

# Enrich existing phrase entries with usage notes (append if missing USAGE:)
EXISTING_USAGE: dict[str, str] = {
    "haw-far": USAGE
    + "Greeting / check-in ('how's it going?'), not a question about physical distance.",
    "no-wahala": USAGE
    + "Reassurance that things are fine or a request is accepted ('no problem').",
    "wetin-de": USAGE
    + "Asks what's going on; shorter cousin of 'wetin de happen'.",
    "abeg": USAGE
    + "Polite request softener ('please'); strength depends on tone and follow-up.",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def merge_notes(old: str | None, usage: str) -> str:
    old = (old or "").strip()
    if USAGE in old:
        return old
    if not old:
        return usage
    return f"{old} | {usage}"


def cmd_apply() -> int:
    entries = load_json(DICT)
    by_id = {e["id"]: e for e in entries}
    added = 0
    updated = 0

    for p in PHRASES:
        eid = p["id"]
        if eid in by_id:
            e = by_id[eid]
            e["notes"] = merge_notes(e.get("notes"), p["notes"])
            for v in p.get("informal_variants", []):
                if v not in e.get("informal_variants", []) and v.casefold() != e["standard_spelling"].casefold():
                    e.setdefault("informal_variants", []).append(v)
            updated += 1
        else:
            entries.append(dict(p))
            by_id[eid] = entries[-1]
            added += 1

    for eid, usage in EXISTING_USAGE.items():
        if eid not in by_id:
            continue
        e = by_id[eid]
        new_notes = merge_notes(e.get("notes"), usage)
        if new_notes != e.get("notes"):
            e["notes"] = new_notes
            updated += 1

    save_json(DICT, entries)
    print(f"Phrase bank: +{added} new, {updated} updated -> {DICT} ({len(entries)} total)")
    return 0


def corpus_files() -> list[Path]:
    files: list[Path] = []
    if SOURCES.is_file():
        meta = load_json(SOURCES)
        for row in meta.get("sources", meta if isinstance(meta, list) else []):
            if not isinstance(row, dict):
                continue
            rel = row.get("path") or row.get("file")
            if not rel:
                continue
            p = ROOT / "data" / "corpus" / rel if not Path(rel).is_absolute() else Path(rel)
            if not p.is_file():
                p = ROOT / rel
            if p.is_file() and p.suffix.lower() in {".txt", ".conllu"}:
                files.append(p)
    # fallback: scan samples + external txt only (skip huge conllu unless registered)
    for sub in ("samples", "external"):
        d = ROOT / "data" / "corpus" / sub
        if d.is_dir():
            files.extend(sorted(d.glob("*.txt")))
    # unique
    seen: set[Path] = set()
    out: list[Path] = []
    for f in files:
        r = f.resolve()
        if r not in seen:
            seen.add(r)
            out.append(f)
    return out


def norm_text(s: str) -> str:
    return re.sub(r"\s+", " ", s.casefold())


def count_phrase(text: str, phrase: str) -> int:
    """Count non-overlapping casefolded phrase occurrences (substring with word-ish bounds)."""
    p = norm_text(phrase)
    if not p:
        return 0
    # escape; allow flexible whitespace inside multiword
    parts = [re.escape(x) for x in p.split()]
    if not parts:
        return 0
    pat = re.compile(r"(?<!\w)" + r"\s+".join(parts) + r"(?!\w)")
    return len(pat.findall(text))


def cmd_evidence() -> int:
    entries = load_json(DICT)
    files = corpus_files()
    if not files:
        print("No corpus .txt files found", file=sys.stderr)
        return 1

    blobs: dict[str, str] = {}
    read_errors: list[str] = []
    for f in files:
        try:
            blobs[f.name] = norm_text(f.read_text(encoding="utf-8", errors="ignore"))
        except OSError as e:
            msg = f"unreadable corpus file {f}: {e}"
            print(msg, file=sys.stderr)
            read_errors.append(msg)
    if read_errors:
        print(f"corpus read failed for {len(read_errors)} file(s)", file=sys.stderr)
        return 1

    # Focus evidence on phrases + words that have informal variants (editor aid)
    targets = [e for e in entries if e.get("part_of_speech") == "phrase" or e.get("informal_variants")]
    rows = []
    for e in targets:
        terms = [e["standard_spelling"], *e.get("informal_variants", [])]
        by_source: Counter[str] = Counter()
        total = 0
        for name, text in blobs.items():
            c = 0
            for t in terms:
                c += count_phrase(text, t)
            if c:
                by_source[name] = c
                total += c
        rows.append(
            {
                "entry_id": e["id"],
                "standard_spelling": e["standard_spelling"],
                "total": total,
                "by_source": dict(by_source),
                "terms_counted": terms,
            }
        )

    rows.sort(key=lambda r: (-r["total"], r["entry_id"]))
    payload = {
        "note": "Internal curator aid only — do not display raw counts on the public website until a documented scoring method exists.",
        "sources_scanned": [f.name for f in files],
        "entries": rows,
    }
    save_json(EVIDENCE, payload)
    nonzero = sum(1 for r in rows if r["total"] > 0)
    print(f"Evidence: {len(rows)} entries scored, {nonzero} with hits -> {EVIDENCE}")
    print(f"Sources: {', '.join(f.name for f in files)}")
    return 0


def cmd_mappings_seed() -> int:
    """Optional: add high-value informal variants to variant_mappings if missing."""
    mappings_data = load_json(MAPPINGS)
    merged = list(mappings_data["mappings"])
    existing = {(m["variant"].casefold(), m["entry_id"]) for m in merged}
    new_rows = []
    for p in PHRASES:
        for v in p.get("informal_variants", []):
            key = (v.casefold(), p["id"])
            if key in existing:
                continue
            if v.casefold() == p["standard_spelling"].casefold():
                continue
            new_rows.append(
                {
                    "variant": v,
                    "entry_id": p["id"],
                    "source": "phrase-bank-option-a",
                    "note": "Phrase-bank informal spelling",
                }
            )
            existing.add(key)
    # also how far etc already on entries — map common English forms if not present
    extras = [
        ("how far", "haw-far", "Greeting phrase English spelling"),
        ("what's happening", "wetin-de-happen", "English gloss spelling"),
    ]
    for v, eid, note in extras:
        key = (v.casefold(), eid)
        if key in existing:
            continue
        new_rows.append({"variant": v, "entry_id": eid, "source": "phrase-bank-option-a", "note": note})
        existing.add(key)

    mappings_data["mappings"].extend(new_rows)
    save_json(MAPPINGS, mappings_data)
    print(f"Mappings: +{len(new_rows)} -> {MAPPINGS}")
    return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] in {"-h", "--help"}:
        print("Usage: phrase_bank.py apply|evidence|mappings|all", file=sys.stderr)
        return 1
    cmd = argv[0]
    if cmd == "apply":
        return cmd_apply()
    if cmd == "evidence":
        return cmd_evidence()
    if cmd == "mappings":
        return cmd_mappings_seed()
    if cmd == "all":
        rc = cmd_apply()
        if rc:
            return rc
        rc = cmd_mappings_seed()
        if rc:
            return rc
        return cmd_evidence()
    print(f"Unknown command: {cmd}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
