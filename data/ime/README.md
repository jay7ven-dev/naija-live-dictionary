# IME lexicon export (II-5a)

Machine-readable digraph + suggestion package for **future** OS/mobile IMEs.

## Regenerate

```bash
python data/export_ime_lexicon.py
python data/export_ime_lexicon.py --self-check
```

## Files

| File | Role |
|------|------|
| `naija-ime-lexicon.json` | Full package (schema, digraphs, acute vowels, suggestions) |
| `naija-ime-lexicon.tsv` | Flat `variant`, `standard`, `entry_id` |

## Rules

- **Read-only for the Live Dictionary.** Do not ingest this folder back into `dictionary.json` or `variant_mappings.json`.
- Regenerated from `data/dictionary.json` + `data/variant_index.json` after lexicon growth / variant apply + index.
- Native Windows/Android/iOS IME apps are **II-5b+** and should consume these artifacts.
