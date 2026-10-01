#!/usr/bin/env python3
"""Minimal rules-normalizer checks (Batch E test health).

Run: python data/test_normalize_rules.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "data"))

from normalize import (  # noqa: E402
    GOLD,
    load_assets,
    normalize_sentence,
    resolve_token_rules,
    self_check,
)


def test_short_token_no_fuzzy() -> None:
    """len<=2 must not fuzzy (parity with resolve_token_rules / normalize.js)."""
    index, by_id, fuzzy_terms, max_d = load_assets()
    for tok in ("be", "a", "to", "of"):
        if index.get(tok):  # already exact in index — skip
            continue
        dec = resolve_token_rules(tok, index, by_id, fuzzy_terms, max_d)
        assert dec["method"] == "unknown", f"{tok!r} -> {dec}"


def test_gold_sentences() -> None:
    index, by_id, fuzzy_terms, max_d = load_assets()
    for src, want in GOLD:
        got = normalize_sentence(
            src,
            backend="rules",
            index=index,
            by_id=by_id,
            fuzzy_terms=fuzzy_terms,
            max_d=max_d,
        )["output"]
        assert got == want, f"{src!r}: got {got!r} want {want!r}"


def test_exact_index_hits() -> None:
    index, by_id, fuzzy_terms, max_d = load_assets()
    for variant, eid in (("pickin", "pikin"), ("book", "buk")):
        dec = resolve_token_rules(variant, index, by_id, fuzzy_terms, max_d)
        assert dec["method"] in ("exact", "identity"), dec
        assert dec["entry_id"] == eid, dec
        assert dec["output"] == by_id[eid], dec


def main() -> int:
    test_exact_index_hits()
    print("OK exact index hits")
    test_short_token_no_fuzzy()
    print("OK short-token no-fuzzy")
    test_gold_sentences()
    print(f"OK gold ({len(GOLD)} sentences)")
    rc = self_check()
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
