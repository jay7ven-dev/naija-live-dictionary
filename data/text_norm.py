#!/usr/bin/env python3
"""Shared Unicode-aware key normalization for dictionary / variant tooling."""
from __future__ import annotations

import unicodedata


def norm_key(s: str) -> str:
    """NFC then casefold — canonical key for spellings and variants."""
    return unicodedata.normalize("NFC", s).casefold()


# Alias used by several older call sites.
norm = norm_key
