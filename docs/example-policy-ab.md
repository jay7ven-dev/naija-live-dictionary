# Disciplined A+B example policy

**Status:** Active (2026-07-23)

## Rule

| Slot | Role | Max |
|------|------|-----|
| Primary (`example_sentences[0]`) | Short teaching example | 1 |
| Secondary (`example_sentences[1]`) | Optional attested line that passes quality gates | 0–1 |
| Quarantine | Rejected / surplus | `data/example_quarantine.json` (not in UI) |

## Commands

```bash
python data/clean_examples.py apply
python data/clean_examples.py report
python schema/validate.py data/dictionary.json
python web/verify.py
```

Future UD ingest must use the gated apply (max 1 filtered secondary):

```bash
python data/enrich_examples.py extract
python data/enrich_examples.py apply   # quality gate on
python data/clean_examples.py apply    # re-rank + quarantine
```

## Out of scope

Public confidence %, auto-merge from quarantine, showing quarantine in the web UI.
