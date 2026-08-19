#!/usr/bin/env python3
"""Broad pronunciation hints from IFRA SNO orthography (not full IPA)."""
from __future__ import annotations

import re
import unicodedata

# Multi-char before single-char (longest match first).
DIGRAPHS = [
    ("sh", "sh"),
    ("ch", "ch"),
    ("ph", "f"),
    ("th", "t"),
    ("wh", "w"),
    ("ng", "ng"),
    ("ai", "eye"),
    ("au", "ow"),
    ("ee", "ee"),
    ("ea", "ee"),
    ("oo", "oo"),
    ("ou", "ow"),
]
SINGLE = {
    "a": "ah",
    "b": "b",
    "c": "k",
    "d": "d",
    "e": "eh",
    "f": "f",
    "g": "g",
    "h": "h",
    "i": "ee",
    "j": "j",
    "k": "k",
    "l": "l",
    "m": "m",
    "n": "n",
    "o": "oh",
    "p": "p",
    "q": "k",
    "r": "r",
    "s": "s",
    "t": "t",
    "u": "oo",
    "v": "v",
    "w": "w",
    "x": "ks",
    "y": "y",
    "z": "z",
}


def _strip_diacritics(s: str) -> str:
    nfd = unicodedata.normalize("NFD", s)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


def broad_pronunciation(word: str) -> str:
    """Return hyphenated broad hint, e.g. pikin -> PEE-kin."""
    if not word:
        return ""
    raw = _strip_diacritics(word).casefold()
    raw = re.sub(r"[^a-z'-]", "", raw)
    if not raw:
        return word
    parts: list[str] = []
    i = 0
    while i < len(raw):
        if raw[i] in "-'":
            i += 1
            continue
        matched = False
        for src, out in DIGRAPHS:
            if raw.startswith(src, i):
                parts.append(out)
                i += len(src)
                matched = True
                break
        if matched:
            continue
        ch = raw[i]
        parts.append(SINGLE.get(ch, ch))
        i += 1
    if not parts:
        return word
    # Stress first syllable for short lemmas
    parts[0] = parts[0].upper()
    return "-".join(parts)
