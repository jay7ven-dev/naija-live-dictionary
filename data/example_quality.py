#!/usr/bin/env python3
"""Shared example quality gates for disciplined A+B (teaching primary + filtered secondary)."""
from __future__ import annotations

import re
import unicodedata

from text_norm import norm

MAX_PRIMARY_LEN = 70
MAX_SECONDARY_LEN = 65
MAX_PUBLIC_EXAMPLES = 2  # primary + at most one secondary

DISFLUENCY = re.compile(
    r"(\.\.\.|…|\b[A-Za-z]-+\.\.\.|\b(eh|erm|errm|um+)\b.*\b(eh|erm|um+)\b)",
    re.IGNORECASE,
)
# Heavy English / transcript glue (CENCOS-like or UD English islands)
ENGLISH_HEAVY = re.compile(
    r"\b(the|that|this|these|those|with|from|have|has|had|was|were|will|would|"
    r"should|could|about|because|which|their|there|what|when|where|your|"
    r"don't|doesn't|didn't|can't|won't|it's|that's|there's|you're)\b",
    re.IGNORECASE,
)
WORD = re.compile(r"[a-zA-ZàáèéìíòóùúÀÁÈÉÌÍÒÓÙÚ]+(?:[-'][a-zA-ZàáèéìíòóùúÀÁÈÉÌÍÒÓÙÚ]+)*")


def strip_diacritics(s: str) -> str:
    nfd = unicodedata.normalize("NFD", s)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


def word_pattern(word: str) -> re.Pattern[str]:
    w = re.escape(word)
    return re.compile(rf"(?<![a-zA-Zàáèéìíòóùú'-]){w}(?![a-zA-Zàáèéìíòóùú'-])", re.IGNORECASE)


def headword_hits(sentence: str, entry: dict) -> bool:
    forms = [entry["standard_spelling"], *entry.get("informal_variants", [])]
    forms.append(entry["id"].replace("-", " "))
    for f in forms:
        f = f.strip()
        if not f:
            continue
        if word_pattern(f).search(sentence):
            return True
        if word_pattern(strip_diacritics(f)).search(strip_diacritics(sentence)):
            return True
    return False


def english_ratio(sentence: str) -> float:
    tokens = WORD.findall(sentence)
    if not tokens:
        return 1.0
    hits = sum(1 for t in tokens if ENGLISH_HEAVY.search(t) or ENGLISH_HEAVY.search(f" {t} "))
    # count English marker tokens via finditer on full string
    markers = len(ENGLISH_HEAVY.findall(sentence))
    return markers / max(len(tokens), 1)


def passes_quality(sentence: str, entry: dict, *, secondary: bool = False) -> tuple[bool, str]:
    """Return (ok, reject_reason)."""
    s = re.sub(r"\s+", " ", (sentence or "").strip())
    if len(s) < 4:
        return False, "too_short"
    limit = MAX_SECONDARY_LEN if secondary else MAX_PRIMARY_LEN
    if len(s) > limit:
        return False, f"too_long>{limit}"
    if DISFLUENCY.search(s):
        return False, "disfluency"
    if not headword_hits(s, entry):
        return False, "headword_not_clear"
    # Strict English load for teaching examples
    ratio = english_ratio(s)
    cap = 0.35 if secondary else 0.25
    if ratio > cap and len(WORD.findall(s)) >= 6:
        return False, f"english_heavy:{ratio:.2f}"
    return True, ""


def score_teaching(sentence: str, entry: dict) -> int:
    """Higher = better primary candidate."""
    s = re.sub(r"\s+", " ", sentence.strip())
    ok, _ = passes_quality(s, entry, secondary=False)
    score = 50 if ok else 0
    # Prefer short clear lines
    score += max(0, 40 - len(s) // 2)
    if headword_hits(s, entry):
        score += 20
    if not DISFLUENCY.search(s):
        score += 10
    score -= int(english_ratio(s) * 30)
    return score
