#!/usr/bin/env python3
"""Build Keyman wordlist.tsv from II-5a IME lexicon export (II-5b)."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IME_JSON = ROOT / "data" / "ime" / "naija-ime-lexicon.json"
OUT = ROOT / "ime" / "keyman" / "naija_sno" / "naija_sno.wordlist.tsv"
KMN = ROOT / "ime" / "keyman" / "naija_sno" / "naija_sno.kmn"

# Standards get higher weight than informal variants for prediction.
COUNT_STANDARD = 100
COUNT_VARIANT = 10


def build_counts() -> Counter[str]:
    if not IME_JSON.is_file():
        raise SystemExit(f"missing {IME_JSON}; run python data/export_ime_lexicon.py first")
    pkg = json.loads(IME_JSON.read_text(encoding="utf-8"))
    counts: Counter[str] = Counter()
    for row in pkg.get("suggestions") or []:
        std = (row.get("standard") or "").strip()
        var = (row.get("variant") or "").strip()
        if std:
            counts[std] = max(counts[std], COUNT_STANDARD)
        if var and var.casefold() != std.casefold():
            counts[var] = max(counts[var], COUNT_VARIANT)
    return counts


def write_wordlist(counts: Counter[str]) -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Keyman wordlist: word <tab> count
    lines = ["word\tcount"]
    for word, n in sorted(counts.items(), key=lambda x: (-x[1], x[0].casefold())):
        if not word or "\t" in word or "\n" in word:
            continue
        lines.append(f"{word}\t{n}")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(lines) - 1


def self_check() -> int:
    errors: list[str] = []
    if not KMN.is_file():
        errors.append(f"missing {KMN}")
    else:
        text = KMN.read_text(encoding="utf-8")
        for dig in ("gb", "kp", "sh", "ch", "zh"):
            if f"'{dig[0]}' + '{dig[1]}'" not in text and f'"{dig}"' not in text:
                # rules use 'g' + 'b' > 'gb'
                needle = f"'{dig[0]}' + '{dig[1]}' > '{dig}'"
                if needle not in text:
                    errors.append(f"kmn missing digraph rule for {dig}")
    if not OUT.is_file():
        errors.append(f"missing {OUT}")
    else:
        rows = OUT.read_text(encoding="utf-8").splitlines()
        if len(rows) < 2:
            errors.append("wordlist empty")
        elif not rows[0].lower().startswith("word"):
            errors.append("wordlist missing header")
    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1
    n = len(OUT.read_text(encoding="utf-8").splitlines()) - 1
    print(f"OK: keyman wordlist {n} words; kmn digraphs present")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Export Keyman wordlist from IME lexicon (II-5b).")
    p.add_argument("--self-check", action="store_true")
    args = p.parse_args(argv)
    if args.self_check:
        return self_check()
    n = write_wordlist(build_counts())
    print(f"Wrote {n} words -> {OUT.relative_to(ROOT)}")
    return self_check()


if __name__ == "__main__":
    raise SystemExit(main())
