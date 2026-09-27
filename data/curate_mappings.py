#!/usr/bin/env python3
"""Curate variant mappings: batch 1 (verified), batch 2 (lin auto), lin review export."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUGGESTIONS = ROOT / "data" / "suggestions.json"
MAPPINGS = ROOT / "data" / "variant_mappings.json"
DICT = ROOT / "data" / "dictionary.json"
BATCH1_OUT = ROOT / "data" / "curated_batch_1.json"
BATCH2_OUT = ROOT / "data" / "curated_batch_2.json"
BATCH3_OUT = ROOT / "data" / "curated_batch_3.json"
BATCH4_OUT = ROOT / "data" / "curated_batch_4.json"
BATCH5_OUT = ROOT / "data" / "curated_batch_5.json"
REVIEW_OUT = ROOT / "docs" / "review-lin-suggestions.md"

# Common English / code-switch tokens in CENCOS — never auto-map via lin
ENGLISH_BLOCKLIST = frozenset(
    """
    is it s t a an the and or but if so as at by to of in on for with from
    be me he she they we you i will would can could should shall do does did
    have has had am are was were not no yes just about think use too top took
    went left right five fifty sit city safe says movie milk bit keke habit
    town rock joke quit bite site fifth pity mess fix coke cause mark fill
    amen mtv fsc alabi asaba benin hausa within taxi skibi neck meal korom
    mere weren whats among fin con were try than reach check three state both
    date bath done she they than reach check three state both date bath
    fry
    """.split()
)

# Known lin false-positive (variant, entry_id) pairs
LIN_PAIR_REJECT = frozenset(
    {
        ("she", "che"),
        ("She", "che"),
        ("they", "dei"),
        ("They", "dei"),
        ("try", "tri"),
        ("Try", "tri"),
        ("three", "tri"),
        ("Three", "tri"),
        ("done", "don"),
        ("than", "dan"),
        ("reach", "rich"),
        ("check", "shek"),
        ("Check", "shek"),
        ("state", "stat"),
        ("State", "stat"),
        ("both", "bot"),
        ("Both", "bot"),
        ("date", "dat"),
        ("bath", "bad"),
        ("fry", "fri"),
    }
)

BATCH_1_VERIFIED: list[tuple[str, str, str]] = [
    ("mey", "mek", "Informal make/let spelling (CENCOS)"),
    ("com", "kom", "Lin rule: come → kom"),
    ("kon", "kom", "Common kom variant (NaijaSenti lexicon)"),
    ("pipol", "pipul", "people spelling variant"),
    ("pipo", "pipul", "people clipping (NaijaSenti)"),
    ("abegi", "abeg", "Reduplicated abeg"),
    ("wating", "wetin", "What spelling variant"),
    ("weyim", "wetin", "What variant"),
    ("noni", "moni", "Money spelling variant"),
    ("deh", "de", "Progressive de variant (NaijaSenti)"),
    ("shebi", "abi", "Tag question variant (se + abi)"),
    ("hebi", "abi", "Tag question variant"),
    ("pesin", "pipul", "Person → people lemma (singular informal)"),
]

# Batch 3 — manual review: lin low-count + English-loan patterns (CENCOS/NaijaSenti)
BATCH_3_VERIFIED: list[tuple[str, str, str]] = [
    ("pic", "pik", "Lin review: pick spelling"),
    ("dise", "dis", "Lin review: this spelling"),
    ("deme", "dem", "Lin review: dem variant"),
    ("gave", "giv", "English past → giv (like give)"),
    ("naw", "nau", "Now spelling variant"),
    ("naww", "nau", "Now emphatic spelling"),
    ("true", "trut", "True → trut (truth lemma family)"),
    ("truth", "trut", "English noun → trut"),
    ("Beacause", "bikos", "CENCOS typo of because → bikos"),
    ("spy", "spie", "Lin review: spy → spie"),
    ("bell", "belle", "Lin review: bell → belle"),
    ("vain", "find", "Lin review: vain → fain (find lemma, not adj fain)"),
]

# Batch 4 — English loans + high-frequency informal spellings (dictionary informal_variants)
BATCH_4_VERIFIED: list[tuple[str, str, str]] = [
    ("watin", "wetin", "What spelling variant (watin)"),
    ("give", "giv", "English give → giv"),
    ("because", "bikos", "English because → bikos"),
    ("becos", "bikos", "Common because spelling (CENCOS)"),
    ("before", "bifo", "English before → bifo"),
    ("tomorrow", "tumoro", "English tomorrow → tumoro"),
    ("something", "somtin", "English something → somtin"),
    ("ting", "somtin", "Thing/something spelling (ting)"),
    ("thing", "somtin", "English thing → somtin (not sing)"),
    ("shey", "abi", "Tag question shey → abi"),
    ("people", "pipul", "English people → pipul"),
    ("money", "moni", "English money → moni"),
    ("come", "kom", "English come → kom"),
]

# Batch 5 — alternate spellings for growth entries + help (index gaps only; no Lin FPs)
BATCH_5_VERIFIED: list[tuple[str, str, str]] = [
    ("happun", "hapen", "happen spelling"),
    ("finsh", "finis", "finish clip/typo"),
    ("clim", "klaim", "climb clip"),
    ("freind", "frend", "friend typo"),
    ("docta", "dokta", "doctor spelling"),
    ("mawning", "mornin", "morning spelling"),
    ("shoutin", "shaut", "shouting clip"),
    ("watta", "wota", "water spelling"),
    ("fon", "fone", "phone clip"),
    ("boddy", "bodi", "body spelling"),
    ("mauth", "mout", "mouth spelling"),
    ("plase", "ples", "place spelling"),
    ("yung", "yong", "young spelling"),
    ("okrah", "okro", "okra spelling"),
    ("fis", "fisi", "fish clip"),
    ("biya", "bia", "beer spelling"),
    ("eazy", "izi", "easy spelling"),
    ("hevy", "hevi", "heavy spelling"),
    ("ogah", "oga", "oga spelling"),
    ("helep", "help", "help spelling"),
    ("helpu", "help", "help spelling"),
    ("neare", "nia", "near spelling"),
    ("dakk", "dak", "dark spelling"),
]


def norm(s: str) -> str:
    return s.casefold()


def load_known_variants(entries: list[dict], mappings: list[dict]) -> set[str]:
    known: set[str] = set()
    for e in entries:
        known.add(norm(e["standard_spelling"]))
        for v in e.get("informal_variants", []):
            known.add(norm(v))
    for m in mappings:
        known.add(norm(m["variant"]))
    return known


def forward_lin_match(standard: str, variant: str) -> bool:
    from lin_variants import generate_variants

    variants = {v.casefold() for v in generate_variants(standard)}
    return variant.casefold() in variants


def lin_suggestions() -> list[dict]:
    data = json.loads(SUGGESTIONS.read_text(encoding="utf-8"))
    rows = [s for s in data.get("suggestions", []) if s.get("method") == "lin"]
    rows.sort(key=lambda x: (-x.get("count", 0), x.get("variant", "")))
    return rows


def assess_lin_row(s: dict, by_id: dict, known: set[str]) -> dict:
    variant = s["variant"]
    eid = s["suggested_entry_id"]
    std = s.get("standard_spelling") or by_id.get(eid, {}).get("standard_spelling", "")
    count = s.get("count", 0)
    block = norm(variant) in ENGLISH_BLOCKLIST
    pair_reject = (variant, eid) in LIN_PAIR_REJECT
    fwd = forward_lin_match(std, variant) if std else False
    mapped = norm(variant) in known
    reasons: list[str] = []
    if mapped:
        reasons.append("already mapped")
    if block:
        reasons.append("english blocklist")
    if pair_reject:
        reasons.append("known false positive")
    if not fwd:
        reasons.append("not forward lin match")
    if count < 5:
        reasons.append("count < 5")
    auto_ok = not reasons and eid in by_id
    return {
        "variant": variant,
        "entry_id": eid,
        "standard_spelling": std,
        "count": count,
        "forward_lin": fwd,
        "blocklisted": block,
        "pair_reject": pair_reject,
        "already_mapped": mapped,
        "auto_batch2": auto_ok,
        "reject_reasons": reasons,
        "sources": s.get("sources", []),
    }


def build_batch5(by_id: dict, known: set[str] | None = None) -> list[dict]:
    """Build batch 5 list. If known is set, skip already-mapped variants (for --apply)."""
    out: list[dict] = []
    seen: set[str] = set()
    for variant, eid, note in BATCH_5_VERIFIED:
        if eid not in by_id:
            continue
        if norm(variant) == norm(by_id[eid]["standard_spelling"]):
            continue
        if norm(variant) in seen:
            continue
        if known is not None and norm(variant) in known:
            continue
        seen.add(norm(variant))
        out.append({"variant": variant, "entry_id": eid, "source": "curated-batch-5", "note": note})
    return out


def build_batch4(by_id: dict, known: set[str] | None = None) -> list[dict]:
    """Build batch 4 list. If known is set, skip already-mapped variants (for --apply)."""
    out: list[dict] = []
    seen: set[str] = set()
    for variant, eid, note in BATCH_4_VERIFIED:
        if eid not in by_id:
            continue
        if norm(variant) == norm(by_id[eid]["standard_spelling"]):
            continue
        if norm(variant) in seen:
            continue
        if known is not None and norm(variant) in known:
            continue
        seen.add(norm(variant))
        out.append({"variant": variant, "entry_id": eid, "source": "curated-batch-4", "note": note})
    return out


def build_batch3(by_id: dict, known: set[str] | None = None) -> list[dict]:
    """Build batch 3 list. If known is set, skip already-mapped variants (for --apply)."""
    out: list[dict] = []
    seen: set[str] = set()
    for variant, eid, note in BATCH_3_VERIFIED:
        if eid not in by_id:
            continue
        if norm(variant) == norm(by_id[eid]["standard_spelling"]):
            continue
        if norm(variant) in seen:
            continue
        if known is not None and norm(variant) in known:
            continue
        seen.add(norm(variant))
        out.append({"variant": variant, "entry_id": eid, "source": "curated-batch-3", "note": note})
    return out


def build_batch1(by_id: dict) -> list[dict]:
    out: list[dict] = []
    seen: set[str] = set()
    for variant, eid, note in BATCH_1_VERIFIED:
        if eid not in by_id:
            continue
        if norm(variant) == norm(by_id[eid]["standard_spelling"]):
            continue
        if norm(variant) in seen:
            continue
        seen.add(norm(variant))
        out.append({"variant": variant, "entry_id": eid, "source": "curated-batch-1", "note": note})
    return out


def build_batch2(by_id: dict, known: set[str]) -> list[dict]:
    approved: list[dict] = []
    seen: set[str] = set()
    for s in lin_suggestions():
        row = assess_lin_row(s, by_id, known)
        if not row["auto_batch2"]:
            continue
        vkey = norm(row["variant"])
        if vkey in seen:
            continue
        seen.add(vkey)
        approved.append(
            {
                "variant": row["variant"],
                "entry_id": row["entry_id"],
                "source": "curated-batch-2-lin",
                "note": f"Lin auto (count={row['count']}, forward-validated)",
            }
        )
    return approved


def write_review(by_id: dict, known: set[str]) -> int:
    lines = [
        "# Lin Suggestion Review (Batch 2)",
        "",
        "Sorted by corpus count (desc). Use this for manual approve/reject before adding to `variant_mappings.json`.",
        "",
        "**Auto batch 2 rule:** `method=lin`, count ≥ 5, forward Lin match, not blocklisted, not already mapped.",
        "",
        "| Count | Variant | → SNO | entry_id | Fwd | Auto? | Notes |",
        "|------:|---------|-------|----------|:---:|-------|-------|",
    ]
    auto_n = 0
    for s in lin_suggestions():
        row = assess_lin_row(s, by_id, known)
        if row["auto_batch2"]:
            auto_n += 1
        notes = ", ".join(row["reject_reasons"]) if row["reject_reasons"] else "—"
        fwd = "yes" if row["forward_lin"] else "no"
        auto = "**Y**" if row["auto_batch2"] else "N"
        lines.append(
            f"| {row['count']} | `{row['variant']}` | {row['standard_spelling']} | `{row['entry_id']}` | {fwd} | {auto} | {notes} |"
        )
    lines.extend(
        [
            "",
            f"**Total lin suggestions:** {len(lin_suggestions())} · **Auto-approved by batch 2 rule:** {auto_n}",
            "",
            "## Manual review candidates (count ≥ 2, not auto)",
            "",
            "These failed auto rules but may still be valid — review individually:",
            "",
        ]
    )
    for s in lin_suggestions():
        row = assess_lin_row(s, by_id, known)
        if row["auto_batch2"] or row["count"] < 2:
            continue
        lines.append(
            f"- `{row['variant']}` → **{row['standard_spelling']}** ({row['entry_id']}), count={row['count']} — {', '.join(row['reject_reasons'])}"
        )
    REVIEW_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote lin review -> {REVIEW_OUT}")
    return len(lin_suggestions())


def merge_mappings(new_rows: list[dict], apply: bool) -> tuple[int, int]:
    mappings_data = json.loads(MAPPINGS.read_text(encoding="utf-8"))
    merged = list(mappings_data["mappings"])
    existing = {(m["variant"], m["entry_id"]) for m in merged}
    added = 0
    for m in new_rows:
        key = (m["variant"], m["entry_id"])
        if key in existing:
            continue
        merged.append(m)
        added += 1
    if apply:
        mappings_data["mappings"] = merged
        MAPPINGS.write_text(json.dumps(mappings_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added, len(merged)


def cmd_batch1(apply: bool) -> int:
    entries = json.loads(DICT.read_text(encoding="utf-8"))
    by_id = {e["id"]: e for e in entries}
    verified = build_batch1(by_id)
    BATCH1_OUT.write_text(
        json.dumps({"batch": 1, "count": len(verified), "mappings": verified}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Batch 1: {len(verified)} mappings -> {BATCH1_OUT}")
    if apply:
        added, total = merge_mappings(verified, True)
        print(f"Applied {added} new (total {total}) -> {MAPPINGS}")
    for m in verified:
        print(f"  {m['variant']!r} -> {by_id[m['entry_id']]['standard_spelling']}")
    return 0


def cmd_batch2(apply: bool) -> int:
    entries = json.loads(DICT.read_text(encoding="utf-8"))
    mappings = json.loads(MAPPINGS.read_text(encoding="utf-8"))["mappings"]
    by_id = {e["id"]: e for e in entries}
    known = load_known_variants(entries, mappings)
    approved = build_batch2(by_id, known)
    BATCH2_OUT.write_text(
        json.dumps({"batch": 2, "count": len(approved), "mappings": approved}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Batch 2 (lin, count>=5): {len(approved)} mappings -> {BATCH2_OUT}")
    if not approved:
        print("No lin suggestions passed auto filters (expected — CENCOS code-switch dominates high-count lin hits).")
    if apply and approved:
        added, total = merge_mappings(approved, True)
        print(f"Applied {added} new (total {total}) -> {MAPPINGS}")
    for m in approved:
        print(f"  {m['variant']!r} -> {by_id[m['entry_id']]['standard_spelling']}")
    return 0


def cmd_batch5(apply: bool) -> int:
    entries = json.loads(DICT.read_text(encoding="utf-8"))
    mappings = json.loads(MAPPINGS.read_text(encoding="utf-8"))["mappings"]
    by_id = {e["id"]: e for e in entries}
    known = load_known_variants(entries, mappings)
    catalog = build_batch5(by_id, known=None)
    to_apply = build_batch5(by_id, known=known)
    BATCH5_OUT.write_text(
        json.dumps({"batch": 5, "count": len(catalog), "mappings": catalog}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Batch 5 (growth alts + help): {len(catalog)} mappings -> {BATCH5_OUT}")
    if apply and to_apply:
        added, total = merge_mappings(to_apply, True)
        print(f"Applied {added} new (total {total}) -> {MAPPINGS}")
    elif apply:
        print(f"All batch 5 variants already in mappings ({len(mappings)} total)")
    for m in catalog:
        print(f"  {m['variant']!r} -> {by_id[m['entry_id']]['standard_spelling']}")
    return 0


def cmd_batch4(apply: bool) -> int:
    entries = json.loads(DICT.read_text(encoding="utf-8"))
    mappings = json.loads(MAPPINGS.read_text(encoding="utf-8"))["mappings"]
    by_id = {e["id"]: e for e in entries}
    known = load_known_variants(entries, mappings)
    catalog = build_batch4(by_id, known=None)
    to_apply = build_batch4(by_id, known=known)
    BATCH4_OUT.write_text(
        json.dumps({"batch": 4, "count": len(catalog), "mappings": catalog}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Batch 4 (manual review): {len(catalog)} mappings -> {BATCH4_OUT}")
    if apply and to_apply:
        added, total = merge_mappings(to_apply, True)
        print(f"Applied {added} new (total {total}) -> {MAPPINGS}")
    elif apply:
        print(f"All batch 4 variants already in mappings ({len(mappings)} total)")
    for m in catalog:
        print(f"  {m['variant']!r} -> {by_id[m['entry_id']]['standard_spelling']}")
    return 0


def cmd_batch3(apply: bool) -> int:
    entries = json.loads(DICT.read_text(encoding="utf-8"))
    mappings = json.loads(MAPPINGS.read_text(encoding="utf-8"))["mappings"]
    by_id = {e["id"]: e for e in entries}
    known = load_known_variants(entries, mappings)
    catalog = build_batch3(by_id, known=None)
    to_apply = build_batch3(by_id, known=known)
    BATCH3_OUT.write_text(
        json.dumps({"batch": 3, "count": len(catalog), "mappings": catalog}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Batch 3 (manual review): {len(catalog)} mappings -> {BATCH3_OUT}")
    if apply and to_apply:
        added, total = merge_mappings(to_apply, True)
        print(f"Applied {added} new (total {total}) -> {MAPPINGS}")
    elif apply:
        print(f"All batch 3 variants already in mappings ({len(mappings)} total)")
    for m in catalog:
        print(f"  {m['variant']!r} -> {by_id[m['entry_id']]['standard_spelling']}")
    return 0


def cmd_review_lin() -> int:
    entries = json.loads(DICT.read_text(encoding="utf-8"))
    mappings = json.loads(MAPPINGS.read_text(encoding="utf-8"))["mappings"]
    by_id = {e["id"]: e for e in entries}
    known = load_known_variants(entries, mappings)
    write_review(by_id, known)
    return 0


def main(argv: list[str]) -> int:
    apply = "--apply" in argv
    if "review-lin" in argv:
        return cmd_review_lin()
    if "batch5" in argv:
        return cmd_batch5(apply)
    if "batch4" in argv:
        return cmd_batch4(apply)
    if "batch3" in argv:
        return cmd_batch3(apply)
    if "batch2" in argv:
        return cmd_batch2(apply)
    if "batch1" in argv:
        return cmd_batch1(apply)
    print(
        "Usage: curate_mappings.py batch1|batch2|batch3|batch4|batch5|review-lin [--apply]\n"
        "  batch1      — human-verified batch 1\n"
        "  batch2      — lin-only, count>=5, forward-validated, blocklist\n"
        "  batch3      — manual review (lin low-count + English loans)\n"
        "  batch4      — English loans + informal spellings from dictionary\n"
        "  batch5      — growth-entry alternate spellings + help\n"
        "  review-lin  — write docs/review-lin-suggestions.md",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
