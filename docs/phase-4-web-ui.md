# Phase 4 — Live Dictionary Web UI

**Status:** Complete (2026-07-10)

Before changing this UI: [`design-ui-resources.md`](design-ui-resources.md) (brainstorm, then pick a skill/resource).

## Run locally

From project root:

```bash
python web/serve.py
```

Open **http://localhost:8765/web/**

Verify data + lookup:

```bash
python web/verify.py
```

## Features

- Browse first 40 entries (alphabetical)
- Search `standard_spelling`, definitions, examples, variants
- **Variant → standard redirect** banner (e.g. `pickin` → `pikin`, `book` → `buk`)
- Uses `data/dictionary.json` + `data/variant_index.json`

## Before deploy

After dictionary or mapping changes:

```bash
python data/collect_variants.py index
python schema/validate.py data/dictionary.json
python web/verify.py
```

## Stack

Static HTML/CSS/JS — no build step. Serve from project root so `fetch('/data/...')` works via relative `../data/` from `/web/`.

## Exit criterion #6

Searchable web interface with browse + search + variant→standard lookup.
