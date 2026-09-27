# Part II-5a — IME lexicon export (design)

**Status:** Implemented with this increment — see `docs/phase-ii-5-ime-export.md`.  
**Prior:** II-4 web compose assist (`docs/phase-ii-4-keyboard-ime.md`)  
**Orthography authority:** IFRA/NLA SNO (D1); digraph/tone inventory matches II-4

## Locked decisions

| Choice | Value |
|--------|--------|
| This increment (**II-5a**) | Regenerable **lexicon export** for future OS/mobile IMEs |
| Native IME (**II-5b+**) | Deferred — Windows TSF / Android / iOS not built here |
| Sources | `data/dictionary.json` + `data/variant_index.json` only |
| Lexicon writes | Export **never** writes dictionary / mappings |
| Digraphs | `ch`, `gb`, `sh`, `kp`, `zh` |
| Acute vowels | `á`, `é`, `í`, `ó`, `ú` |
| Artifacts | `data/ime/naija-ime-lexicon.json` + `.tsv` |

## Goal

1. Freeze a machine-readable digraph + suggestion contract that OS/mobile IME packages can consume later.  
2. Keep export regenerable from the Live Dictionary so IMEs stay aligned with curated SNO data.  
3. Do **not** ship installers or system key hooks in II-5a.

---

## Phase II-5a — Export

### In

1. CLI: `python data/export_ime_lexicon.py`  
2. JSON package: schema version, timestamps, source paths, counts, digraphs, acute vowels, suggestion rows `{variant, entry_id, standard}`.  
3. TSV sibling: `variant\tstandard\tentry_id` for simple consumers.  
4. `data/ime/README.md` — regenerate command; not for auto-ingest into the dictionary.  
5. Phase note + `PROJECT.md` II-5a Done / II-5b+ Deferred.  
6. Verify: digraph count 5; `len(suggestions) == len(variant_index)`.

### Out

Windows TSF, Android InputMethodService, iOS keyboard extension, store listings, Keyman/Gboard layout projects (those may consume the export in II-5b+).

### Check

```bash
python data/export_ime_lexicon.py
python data/export_ime_lexicon.py --self-check
python web/verify.py
```

---

## Phase II-5b+ — Native IME (deferred)

Consume `data/ime/naija-ime-lexicon.json` (or TSV) in a platform package. Still no silent lexicon writes from the IME.

## Spec review gate

**Approved by plan choice** (export-only, 2026-09-27). Implementation follows this file.
