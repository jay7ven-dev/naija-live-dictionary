# Canonical documentation index

**Single scientific source of truth:** [`manuscripts/naija-live-dictionary.md`](manuscripts/naija-live-dictionary.md) (snapshot **2026-10-01**; Part I lexicon + Part II Fix spelling primary / Advanced MT / Keyman)

Phase logs under `docs/phase-*.md` and `docs/phase-ii-*.md` are execution notes. If a number or policy conflicts with the manuscript or live validators, trust **validators first**, then the manuscript.

## Audience guides (derived from the manuscript)

| Audience | Guide |
|----------|--------|
| Researchers | [`canonical/for-researchers.md`](canonical/for-researchers.md) |
| Developers | [`canonical/for-developers.md`](canonical/for-developers.md) |
| General users | [`canonical/for-users.md`](canonical/for-users.md) |

## Supporting project docs (still valid)

| Topic | File |
|-------|------|
| Schema | `dictionary-entry-schema.md` |
| Citations (BibTeX) | `citation-pack.md` |
| Licensing (D4) | `d4-public-release-licensing.md` |
| Ethics (D3) | `phase-3-data-collection-ethics.md` |
| Variant pipeline | `phase-3-variant-pipeline.md` |
| Live growth | [`live-growth.md`](live-growth.md) |
| Part II normalizer | `phase-ii-1-normalizer.md`, `phase-ii-2-normalizer-model.md` |
| Part II translate (Advanced MT) | `phase-ii-3-translate-harden.md` |
| II-4 compose (removed) | `phase-ii-4-keyboard-ime.md` |
| II-5a / II-5b | `phase-ii-5-ime-export.md`, `phase-ii-5b-keyman.md` |
| Design / UI resources | [`design-ui-resources.md`](design-ui-resources.md) — consult before any `web/` or UI work |

Public release: [`public-release-checklist.md`](public-release-checklist.md) · [`../LICENSE`](../LICENSE) · [`../README.md`](../README.md)

## Live metrics (re-run)

```bash
python schema/validate.py data/dictionary.json
python web/verify.py
python data/normalize.py --self-check
python data/normalize.py --eval data/eval/messy_pidgin_sample.jsonl
python data/enrich_examples.py report
```
