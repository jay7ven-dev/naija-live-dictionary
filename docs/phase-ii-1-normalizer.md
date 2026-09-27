# Phase II-1 — Rule-based sentence normalizer

**Status:** Implemented (2026-09-23)  
**Spec:** `docs/superpowers/specs/2026-09-22-part-ii-normalizer-design.md`  
**Pillars:** Part II · 2 (normalizer) + setup for 3 (model compare later)

---

## Delivered

| Piece | Path |
|-------|------|
| Core + CLI | `data/normalize.py` |
| Web UI | `web/normalize.html`, `web/normalize.js` |
| Link from dictionary | `web/index.html` footer → Normalize |

**Lookup order (per token):** exact `variant_index` → fuzzy ≤ 2 → leave + `unknown`.  
Resolves entry ids to `standard_spelling`. Does **not** write the lexicon.

## Commands

```bash
python data/normalize.py "Di pickin wan book."
python data/normalize.py --json "Di pickin wan book."
python data/normalize.py --self-check
python web/verify.py
python web/serve.py   # http://localhost:8765/web/normalize.html
```

## Next

Phase II-2 — trained backend + `--backend model` + held-out eval vs rules (after II-1 accepted).
