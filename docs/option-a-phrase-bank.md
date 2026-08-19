# Option A — Phrase bank + usage notes + internal evidence

**Status:** Done (2026-07-22)  
**Approved from:** vision-scrutinize decision surface (Option 1 / A)

## What shipped

1. **Phrase bank** — 11 new `phrase` entries (SNO headwords + informal variants).
2. **Usage notes** — discourse explanations in `notes` (prefix `Usage:`) for new phrases + `haw-far`, `no-wahala`, `wetin-de`, `abeg`.
3. **Internal evidence** — `data/evidence_counts.json` from project corpus files only. **Not** shown in the web UI.

## Commands

```bash
python data/phrase_bank.py all          # apply + mappings + evidence
python data/collect_variants.py apply
python data/collect_variants.py index
python schema/validate.py data/dictionary.json
python web/verify.py
```

## Out of scope (still rejected)

Public confidence %, social scrape, LLM example factory, Living KB rebuild.
