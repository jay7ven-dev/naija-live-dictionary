# Corpus input

Place UTF-8 `.txt` samples here. Register each file in `sources.json` before extract.
`.conllu` UD treebanks may be registered for example enrichment, but `extract` skips them
(raw CoNLL-U otherwise pollutes candidates with AlignBegin / Gloss / metadata tokens).

See `docs/phase-3-data-collection-ethics.md` for admissible sources.

```bash
python data/collect_variants.py extract
```
