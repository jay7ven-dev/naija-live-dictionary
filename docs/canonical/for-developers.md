# For developers

Derived from [`../manuscripts/naija-live-dictionary.md`](../manuscripts/naija-live-dictionary.md). Canonical data file: `data/dictionary.json`.

## Architecture (keep this)

```
IFRA SNO headwords → data/dictionary.json
                   → data/variant_mappings.json (human-approved)
                   → data/collect_variants.py (extract|suggest|apply|index)
                   → data/variant_index.json + data/fuzzy_lookup.json
                   → web/ (search + variant→standard + fuzzy)
```

Do **not** auto-apply `suggestions.json` into the dictionary.

## Day-to-day commands

```bash
python schema/validate.py data/dictionary.json
python data/collect_variants.py extract
python data/collect_variants.py suggest    # pending only
# edit / curate_mappings.py batchN --apply
python data/collect_variants.py apply
python data/collect_variants.py index
python web/verify.py
python web/serve.py                        # http://localhost:8765/web/
python export/tei_lex0.py
```

## Schema

Machine schema: `schema/entry.schema.json`  
Human doc: `../dictionary-entry-schema.md`

## Web UI notes

- Serve from project root (`web/serve.py`), not by opening `index.html` as a `file://` URL (CORS blocks modules/data).
- Root `/` redirects to `/web/`.
- Docs live under `/web/docs/` (Layers 2–5).

## Ethics / licensing gates

- Corpus policy: `../phase-3-data-collection-ethics.md`
- Public release tiers: `../d4-public-release-licensing.md`
- Register every corpus file in `data/corpus/sources.json`
