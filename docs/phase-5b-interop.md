# Phase 5b — Interop & Documentation

**Status:** Active (2026-07-10)  
**Research bundle:** R5 (TEI Lex-0 export + citation pack)

---

## Goals

| Deliverable | Path |
|-------------|------|
| TEI Lex-0 export (one-way from JSON) | `export/tei_lex0.py` → `export/naija-dictionary.lex0.xml` |
| Export verification | `export/verify_tei.py` |
| Academic citation pack | `docs/citation-pack.md` |

**Unchanged:** `data/dictionary.json` remains the canonical runtime source for web UI and pipelines.

---

## Export

```bash
python export/tei_lex0.py
python export/verify_tei.py
```

Custom output path:

```bash
python export/tei_lex0.py path/to/output.xml
```

---

## TEI mapping

| JSON field | TEI Lex-0 |
|------------|-----------|
| `id` | `entry/@xml:id` |
| `standard_spelling` | `form[@type=lemma]/orth` |
| `part_of_speech` | `gramGrp/pos` |
| `definitions[]` | `sense/def` (one sense per gloss) |
| `example_sentences[]` | `cit[@type=example]/quote` |
| `informal_variants[]` | `form[@type=variant]/orth` |
| `pronunciation` | `form[@type=pronunciation]/orth` |
| `notes` | `note` |

---

## Citations

See `docs/citation-pack.md` for BibTeX entries covering IFRA SNO, NaijaSenti, CENCOS, Lin et al. (2024), and this project.

---

## Validation

```bash
python schema/validate.py data/dictionary.json
python export/tei_lex0.py
python export/verify_tei.py
python web/verify.py
```
