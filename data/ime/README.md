# IME lexicon export (II-5a)

Machine-readable digraph + suggestion package for Keyman and other OS/mobile IMEs.

## Regenerate

```bash
python data/export_ime_lexicon.py
python data/export_ime_lexicon.py --self-check
# After lexicon growth, also refresh the Keyman wordlist (II-5b):
python data/export_keyman_wordlist.py
```

## Files

| File | Role |
|------|------|
| `naija-ime-lexicon.json` | Full package (schema, digraphs, acute vowels, suggestions) |
| `naija-ime-lexicon.tsv` | Flat `variant`, `standard`, `entry_id` |

## Consumer (II-5b)

Keyman keyboard sources: `ime/keyman/naija_sno/` — digraph/acute `.kmn`, package `.kps`, wordlist from `data/export_keyman_wordlist.py`. See `docs/phase-ii-5b-keyman.md`.

## Rules

- **Read-only for the Live Dictionary.** Do not ingest this folder back into `dictionary.json` or `variant_mappings.json`.
- Regenerated from `data/dictionary.json` + `data/variant_index.json` after lexicon growth / variant apply + index.
- Native TSF / Android / iOS apps (II-5c+) may also consume these artifacts; Keyman is the shipped II-5b path.
