# Phase 5a — Live Dictionary Hardening

**Status:** Active (2026-07-10)  
**Research bundle:** R1 + R2 + R3 (approved from Phase X literature survey)

---

## Goals

| ID | Feature | Artifact |
|----|---------|----------|
| **R1** | Lin-inspired variant **suggestions** (human gate) | `data/lin_variants.py`, `collect_variants.py suggest` → `suggestions.json` |
| **R2** | Fuzzy “Did you mean?” after exact index miss | `data/fuzzy_lookup.json`, `web/app.js` |
| **R3** | Licensed corpus ingest (NaijaSenti + CENCOS) | `data/ingest_external.py`, `data/corpus/external/` |

**Unchanged:** IFRA SNO headwords, `variant_mappings.json` human approval, schema core.

---

## R1 — Variant suggester

```bash
python data/collect_variants.py extract
python data/collect_variants.py suggest
# Review data/suggestions.json → add approved rows to variant_mappings.json
python data/collect_variants.py apply
python data/collect_variants.py index
```

Suggestions are **never auto-applied**. Reference: Lin et al. LREC-COLING 2024 orthographic variation taxonomy (subset implemented in `lin_variants.py`).

---

## R2 — Fuzzy lookup tier

1. Exact match via `variant_index.json` (unchanged).
2. Substring search on entries (unchanged).
3. If zero hits: Levenshtein distance ≤ 2 over `fuzzy_lookup.json` terms.

Regenerate fuzzy index after apply/index:

```bash
python data/collect_variants.py index
```

---

## R3 — External corpora

```bash
python data/ingest_external.py          # both
python data/ingest_external.py naijasenti
python data/ingest_external.py cencos
python data/collect_variants.py extract
```

| Corpus | Source | License note |
|--------|--------|--------------|
| NaijaSenti pcm_train | hausanlp/NaijaSenti | Cite Muhammad et al. 2022 |
| CENCOS | Zenodo 7314016 | Cite Agbo & Plag 2022 |

Manual fallback: place UTF-8 `.txt` under `data/corpus/external/` and register in `sources.json`.

Optional full NaijaSenti: `pip install datasets` then re-run `ingest_external.py naijasenti` (uses Hugging Face `HausaNLP/NaijaSenti-Twitter` pcm split).

---

## Validation

```bash
python schema/validate.py data/dictionary.json
python web/verify.py
python web/serve.py   # http://localhost:8765/web/
```

---

## Open decision

**D4** — **RESOLVED** — see `docs/d4-public-release-licensing.md` (tiered public-release policy; IFRA guide body not redistributed without permission).
