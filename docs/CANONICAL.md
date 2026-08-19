# Canonical documentation index

**Single scientific source of truth:** [`manuscripts/naija-live-dictionary.md`](manuscripts/naija-live-dictionary.md)

Phase logs under `docs/phase-*.md` are historical execution notes. If a number or policy conflicts with the manuscript or live validators, trust **validators first**, then the manuscript.

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
| Design / UI resources | [`design-ui-resources.md`](design-ui-resources.md) — consult before any `web/` or UI work; brainstorm then pick a skill/resource from that file |

Public release: [`public-release-checklist.md`](public-release-checklist.md) · [`../LICENSE`](../LICENSE) · [`../README.md`](../README.md)

## Live metrics (re-run)

```bash
python schema/validate.py data/dictionary.json
python web/verify.py
python data/enrich_examples.py report
```
