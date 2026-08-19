# Phase 5c — North Star NLP Seed

**Status:** Active (2026-07-10)  
**Research bundle:** R6 + R7 (pronunciation enrichment + FST variant rules)

---

## Goals

| ID | Feature | Artifact |
|----|---------|----------|
| **R6** | Broad pronunciation hints from SNO orthography | `data/g2p_hints.py`, `data/enrich_pronunciation.py` |
| **R6** | Common Voice pcm sentence ingest (optional) | `enrich_pronunciation.py ingest-cv` |
| **R7** | Pynini FST variant generator (fallback: `lin_variants.py`) | `data/fst_variants.py` |
| **R7** | FST-aware suggest mode | `collect_variants.py suggest` / `fst-suggest` |

**Unchanged:** JSON schema core; pronunciation is optional; variant mappings still human-approved.

---

## R6 — Pronunciation enrichment

Rule-based broad hints (hyphenated respelling, not full IPA):

```bash
python data/enrich_pronunciation.py apply
python data/enrich_pronunciation.py report
```

Optional Common Voice pcm sentences (CC0):

```bash
python data/enrich_pronunciation.py ingest-cv
```

Requires network; falls back gracefully if HF datasets server unavailable.

---

## R7 — FST variant rules

Install optional dependency for compiled FST rules:

```bash
pip install -r requirements-optional.txt
```

Without `pynini`, `fst_variants.py` delegates to `lin_variants.py`.

```bash
python data/collect_variants.py suggest   # uses FST when available
```

---

## Web UI

Entries with `pronunciation` show a hint line on result cards after `apply`.

---

## Validation

```bash
python data/enrich_pronunciation.py apply
python schema/validate.py data/dictionary.json
python export/tei_lex0.py
python export/verify_tei.py
python web/verify.py
```

---

## North Star note

Full ASR models, autocorrect, and trained normalizers remain **Part II** (`PROJECT.md` §11). Phase 5c seeds data and sidecar tools only.
