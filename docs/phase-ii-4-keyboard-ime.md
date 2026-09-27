# Phase II-4 — Keyboard / IME (web compose assist)

**Status:** Implemented (2026-09-27)  
**Spec:** `docs/superpowers/specs/2026-09-27-part-ii-4-keyboard-ime-design.md`

## Delivered

- Shared `web/compose.js`: digraph inserts (`gb` `kp` `sh` `ch` `zh`) + high-tone vowels (`á é í ó ú`)
- **Primary:** `web/normalize.html` — digraph panel + live prefix suggestions from `variant_index.json` (accept replaces current token with SNO standard)
- **Secondary:** `web/index.html` — digraph panel only (search already has GOV.UK-style prefix suggest)
- Does not auto-write the lexicon; does not replace English → Pidgin / Fix spelling

## Check

```bash
python web/serve.py
# /web/normalize.html — insert digraph; type a prefix → pick suggestion
# /web/ — digraph insert into search
python web/verify.py
```

## Later

OS / mobile IME packaging remains II-5+ (same digraph + export contract).
