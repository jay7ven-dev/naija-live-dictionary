#!/usr/bin/env python3
"""Disciplined A+B example cleanup: 1 primary + optional 1 filtered secondary; quarantine rest."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from example_quality import (
    MAX_PUBLIC_EXAMPLES,
    norm,
    passes_quality,
    score_teaching,
)

ROOT = Path(__file__).resolve().parent.parent
DICT = ROOT / "data" / "dictionary.json"
QUARANTINE = ROOT / "data" / "example_quarantine.json"
UD_TAG = "UD_Naija-NSC example (CC BY-SA 4.0)"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def strip_ud_tag(notes: str | None) -> str | None:
    if not notes:
        return None
    text = notes.replace(UD_TAG, "")
    parts = [p.strip() for p in text.split("|") if p.strip()]
    cleaned = " | ".join(parts).strip(" |")
    return cleaned or None


def ensure_ud_tag(notes: str | None) -> str:
    base = (notes or "").strip()
    if UD_TAG in base:
        return base
    return f"{base} | {UD_TAG}".strip(" |") if base else UD_TAG


def clean_entry(entry: dict) -> tuple[list[str], list[dict], bool]:
    """Return (kept_examples, quarantine_rows, kept_secondary_ud_like)."""
    examples = list(entry.get("example_sentences") or [])
    if not examples:
        return [], [], False

    ranked = sorted(examples, key=lambda s: -score_teaching(s, entry))
    primary = None
    for s in ranked:
        ok, _ = passes_quality(s, entry, secondary=False)
        if ok:
            primary = s
            break
    if primary is None:
        # Schema requires ≥1 example: keep shortest as last-resort primary
        primary = min(examples, key=len)

    kept = [primary]
    quarantine: list[dict] = []
    secondary = None

    for s in examples:
        if norm(s) == norm(primary):
            continue
        ok, reason = passes_quality(s, entry, secondary=True)
        if ok and secondary is None and norm(s) != norm(primary):
            secondary = s
            continue
        quarantine.append(
            {
                "entry_id": entry["id"],
                "sentence": s,
                "reason": reason if not ok else "over_secondary_cap",
            }
        )

    if secondary:
        kept.append(secondary)

    # Any extras already handled; if primary was last-resort and others failed, quarantined above
    assert 1 <= len(kept) <= MAX_PUBLIC_EXAMPLES
    return kept, quarantine, secondary is not None


def cmd_apply() -> int:
    entries = load_json(DICT)
    all_q: list[dict] = []
    changed = 0
    with_secondary = 0

    for entry in entries:
        before = list(entry.get("example_sentences") or [])
        kept, qrows, has_sec = clean_entry(entry)
        all_q.extend(qrows)
        if has_sec:
            with_secondary += 1

        had_ud = "UD_Naija" in (entry.get("notes") or "")
        cleaned = strip_ud_tag(entry.get("notes"))
        if has_sec and had_ud:
            entry["notes"] = ensure_ud_tag(cleaned)
        elif cleaned:
            entry["notes"] = cleaned
        elif "notes" in entry:
            del entry["notes"]

        if [norm(x) for x in before] != [norm(x) for x in kept]:
            changed += 1
        entry["example_sentences"] = kept

    save_json(
        QUARANTINE,
        {
            "policy": "disciplined-A+B",
            "note": "Rejected or surplus examples — not shown in web UI. Do not auto-merge back without review.",
            "count": len(all_q),
            "items": all_q,
        },
    )
    save_json(DICT, entries)
    print(
        f"Cleaned {changed} entries; {with_secondary} with secondary; "
        f"{len(all_q)} quarantined -> {QUARANTINE}"
    )
    return 0


def cmd_report() -> int:
    entries = load_json(DICT)
    n1 = sum(1 for e in entries if len(e.get("example_sentences") or []) == 1)
    n2 = sum(1 for e in entries if len(e.get("example_sentences") or []) >= 2)
    n_ud = sum(1 for e in entries if "UD_Naija" in (e.get("notes") or ""))
    q = load_json(QUARANTINE) if QUARANTINE.is_file() else {}
    print(f"{len(entries)} entries; {n1} primary-only; {n2} with secondary; {n_ud} UD-tagged notes")
    print(f"Quarantine items: {q.get('count', 0)}")
    return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] in {"-h", "--help"}:
        print("Usage: clean_examples.py apply|report", file=sys.stderr)
        return 1
    if argv[0] == "apply":
        return cmd_apply()
    if argv[0] == "report":
        return cmd_report()
    print(f"Unknown: {argv[0]}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
