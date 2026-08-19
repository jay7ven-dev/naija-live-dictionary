# Phase 3 — Variant Mapping Pipeline

**Status:** Active (2026-07-10)  
**Exit criteria:** #4 (variants linked), #5 (ethics doc — see `phase-3-data-collection-ethics.md`)

---

## Goal

Find informal spellings in real-world Pidgin text and link them to IFRA SNO headwords via `informal_variants[]` on dictionary entries.

---

## Pipeline (4 steps)

```
Corpus (.txt)  →  extract  →  candidates.json  →  curate  →  variant_mappings.json
                                                                    ↓
                                                          apply → dictionary.json
                                                                    ↓
                                                          validate.py
```

| Step | Command / artifact | Output |
|------|-------------------|--------|
| 1. Ingest | Add UTF-8 text to `data/corpus/`; register in `sources.json` | Raw samples |
| 2. Extract | `python data/collect_variants.py extract` | `data/candidates.json` |
| 2b. Suggest | `python data/collect_variants.py suggest` | `data/suggestions.json` (Phase 5a) |
| 3. Curate | Edit `data/variant_mappings.json` | Approved `{variant → entry_id}` |
| 4. Apply | `python data/collect_variants.py apply` | Updated `data/dictionary.json` |

---

## Matching rules

- **Case:** matching is case-insensitive for ASCII letters; diacritics preserved when present.
- **Standard form:** never added as a variant of itself.
- **Unknown tokens:** listed in `candidates.json` with `status: unmatched` for human review.
- **Already linked:** tokens already in dictionary `standard_spelling` or any entry’s `informal_variants` are skipped in candidates.
- **Multi-word variants:** store as single string (e.g. `sharp sharp`, `pickin dem`) when observed in corpus.

---

## Variant mapping file

`data/variant_mappings.json`:

```json
{
  "mappings": [
    { "variant": "dey", "entry_id": "de-copula", "source": "corpus-social-01", "note": "locative; maps to SNO déy" }
  ]
}
```

- `entry_id` must exist in `data/dictionary.json`.
- `source` should match `sources.json` id when from corpus.

---

## Index (for Phase 4 UI)

After `apply`, build lookup index:

```bash
python data/collect_variants.py index
```

Writes `data/variant_index.json`: `{ "dey": "de-copula", "pickin": "pikin", ... }` → resolves variant to entry `id`.

---

## Orthography mapping hints (IFRA-primary)

| Informal pattern | SNO target | Example |
|------------------|------------|---------|
| English loan spelling | SNO phonetic | `book` → `buk` |
| Unmarked tone | Marked when disambiguating | `dey` → `déy` (locative) |
| Hyphenated reduplication | Joined (IFRA §4.3) | `sharp-sharp` → `shapshap` |
| Naija Guru plural | SNO *dem* hyphen | `pickin dem` → `pikin-dem` (phrase variant → `pikin`) |

---

## Files

| Path | Role |
|------|------|
| `data/corpus/` | Input text samples |
| `data/corpus/sources.json` | Ethics manifest |
| `data/candidates.json` | Extract output (review queue) |
| `data/variant_mappings.json` | Approved mappings |
| `data/variant_index.json` | Flat lookup for search UI |
| `data/collect_variants.py` | Extract / apply / index |

---

## Phase 3 checklist

- [x] Pipeline documented
- [x] Ethics policy (D3) documented
- [x] Sample corpus + sources manifest
- [x] Extract / apply / index tooling
- [x] Initial mappings applied to dictionary
