#!/usr/bin/env python3
"""Pynini FST variant generator (R7). Falls back to lin_variants when pynini absent."""
from __future__ import annotations

try:
    import pynini
    from pynini import cdrewrite, cross, union
    from pynini.lib import utf8

    HAS_PYNINI = True
except ImportError:
    pynini = None
    HAS_PYNINI = False

from lin_variants import generate_variants as lin_generate


def _build_fst():
    sigma = utf8.VALID_UTF8_CHAR.star
    rules = union(
        cross("th", "t"),
        cross("th", "d"),
        cross("ph", "f"),
        cross("wh", "w"),
        cross("ch", "sh"),
        cross("ck", "k"),
        cross("ee", "i"),
        cross("ea", "i"),
        cross("ble", "bol"),
        cross("c", "k"),
        cross("k", "c"),
    )
    return cdrewrite(rules, "", "", sigma).closure()


_FST = None


def fst_available() -> bool:
    return HAS_PYNINI


def generate_variants(word: str, max_variants: int = 24) -> list[str]:
    if not word or not word.replace("-", "").replace("'", "").isalpha():
        return []
    if not HAS_PYNINI:
        return lin_generate(word, max_variants=max_variants)
    global _FST
    if _FST is None:
        _FST = _build_fst()
    base = word.casefold()
    seen: set[str] = {base}
    out: list[str] = []
    try:
        lattice = pynini.compose(base, _FST)
        for path in pynini.shortestpath(lattice, nshortest=max_variants * 2).paths():
            s = str(path).casefold()
            if s != base and s not in seen:
                seen.add(s)
                out.append(s)
                if len(out) >= max_variants:
                    break
    except Exception:
        return lin_generate(word, max_variants=max_variants)
    if not out:
        return lin_generate(word, max_variants=max_variants)
    return sorted(out)[:max_variants]


def suggest_entry_for_token(token: str, standards: list[tuple[str, str]]) -> tuple[str, str] | None:
    """Map token via FST-generated variants against dictionary standards."""
    t = token.casefold()
    std_by_norm = {s.casefold(): eid for eid, s in standards}
    if t in std_by_norm:
        return std_by_norm[t], "exact"
    for eid, spelling in standards:
        s = spelling.casefold()
        if t in {v.casefold() for v in generate_variants(spelling)}:
            return eid, "fst" if HAS_PYNINI else "lin"
        if s in {v.casefold() for v in generate_variants(token)}:
            return eid, "fst" if HAS_PYNINI else "lin"
    return None
