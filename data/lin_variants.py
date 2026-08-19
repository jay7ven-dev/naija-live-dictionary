#!/usr/bin/env python3
"""Lin et al. (2024)-inspired PCM orthographic variant generators (suggest-only)."""
from __future__ import annotations

import re

# Subset of Table 1 patterns — phonetic edits common in Nigerian Pidgin text.
SUBSTITUTIONS = [
    ("th", "t"),
    ("th", "d"),
    ("ph", "f"),
    ("wh", "w"),
    ("ch", "sh"),
    ("ck", "k"),
    ("qu", "kw"),
]
SINGLE_CHAR = [
    ("c", "k"),
    ("k", "c"),
    ("y", "i"),
    ("i", "y"),
    ("f", "v"),
]
SUFFIX_RULES = [
    ("ble", "bol"),
    ("ple", "pol"),
    ("ight", "ite"),
    ("ough", "of"),
]
VOWEL_CLUSTERS = [
    ("ee", "i"),
    ("ea", "i"),
    ("eo", "i"),
    ("au", "o"),
    ("oo", "u"),
]


def _apply_at(word: str, old: str, new: str, position: str) -> set[str]:
    w = word.casefold()
    out: set[str] = set()
    if position == "initial" and w.startswith(old):
        out.add(new + w[len(old) :])
    elif position == "medial":
        idx = w.find(old)
        while idx != -1:
            if 0 < idx < len(w) - len(old):
                out.add(w[:idx] + new + w[idx + len(old) :])
            idx = w.find(old, idx + 1)
    elif position == "final" and w.endswith(old):
        out.add(w[: -len(old)] + new)
    elif position == "all":
        if old in w:
            out.add(w.replace(old, new))
    return out


def generate_variants(word: str, max_variants: int = 24) -> list[str]:
    """Return plausible informal spellings for a standard SNO headword."""
    if not word or not re.match(r"^[a-zA-Zàáèéìíòóùú'-]+$", word):
        return []
    base = word.casefold()
    seen: set[str] = {base}
    queue: list[str] = [base]

    while queue and len(seen) < max_variants + 1:
        w = queue.pop(0)
        candidates: set[str] = set()
        for old, new in SUBSTITUTIONS:
            for pos in ("initial", "medial", "final", "all"):
                candidates |= _apply_at(w, old, new, pos)
        for old, new in SINGLE_CHAR:
            candidates |= _apply_at(w, old, new, "all")
        for old, new in SUFFIX_RULES:
            candidates |= _apply_at(w, old, new, "final")
        for old, new in VOWEL_CLUSTERS:
            candidates |= _apply_at(w, old, new, "medial")
            candidates |= _apply_at(w, old, new, "all")
        # silent e deletion (come→kom pattern)
        if len(w) > 3 and w.endswith("e"):
            candidates.add(w[:-1])
        for c in candidates:
            if c and c not in seen and c != base:
                seen.add(c)
                queue.append(c)
                if len(seen) >= max_variants + 1:
                    break
    seen.discard(base)
    return sorted(seen)[:max_variants]


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cost = 0 if ca == cb else 1
            cur.append(min(cur[j - 1] + 1, prev[j] + 1, prev[j - 1] + cost))
        prev = cur
    return prev[-1]


def suggest_entry_for_token(
    token: str, standards: list[tuple[str, str]], max_edit: int = 2
) -> tuple[str, str] | None:
    """Map token to (entry_id, method) via Lin rules + edit distance."""
    t = token.casefold()
    std_by_norm = {s.casefold(): eid for eid, s in standards}
    if t in std_by_norm:
        return std_by_norm[t], "exact"
    for eid, spelling in standards:
        s = spelling.casefold()
        if t in {v.casefold() for v in generate_variants(spelling)}:
            return eid, "lin"
        if s in {v.casefold() for v in generate_variants(token)}:
            return eid, "lin"
    best: tuple[str, str, int] | None = None
    for eid, spelling in standards:
        s = spelling.casefold()
        if abs(len(s) - len(t)) > max_edit:
            continue
        d = levenshtein(t, s)
        if d <= max_edit and (best is None or d < best[2]):
            best = (eid, "fuzzy", d)
    if best:
        return best[0], best[1]
    return None
