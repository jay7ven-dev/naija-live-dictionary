# Phase II-5a — IME lexicon export

**Status:** Implemented (2026-09-27)  
**Spec:** `docs/superpowers/specs/2026-09-27-part-ii-5-ime-export-design.md`

## Delivered

- `data/export_ime_lexicon.py` — regenerates export from Live Dictionary assets
- `data/ime/naija-ime-lexicon.json` — digraphs, acute vowels, suggestion rows
- `data/ime/naija-ime-lexicon.tsv` — `variant / standard / entry_id`
- Does **not** write `dictionary.json` or mappings
- Native Keyman keyboard is **II-5b** (`docs/phase-ii-5b-keyman.md`); TSF / Android / iOS remain **II-5c+**

## Check

```bash
python data/export_ime_lexicon.py
python data/export_ime_lexicon.py --self-check
python web/verify.py
```
