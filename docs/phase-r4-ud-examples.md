# Phase R4 — UD_Naija-NSC Example Enrichment

**Status:** Done (2026-07-10)  
**License:** [UD_Naija-NSC](https://github.com/UniversalDependencies/UD_Naija-NSC) — CC BY-SA 4.0

**Run summary:** 8,790 UD sentences parsed → 519 examples applied to 264/306 entries (max 3/entry). `web/verify.py` and TEI export pass.

---

## Goal

Add authentic spoken Naijá example sentences to `dictionary.json` `example_sentences[]` from the Naija Treebank. Schema and headwords unchanged.

---

## Pipeline

```bash
python data/enrich_examples.py ingest    # download CoNLL-U splits
python data/enrich_examples.py extract   # -> data/example_suggestions.json
python data/enrich_examples.py apply     # merge (max 2 new / entry, 3 total)
python schema/validate.py data/dictionary.json
python export/tei_lex0.py
```

---

## Matching rules

1. Prefer `# text_ortho` from CoNLL-U (cleaner than `# text` with disfluency markers).
2. Match entry when **SNO surface form** appears in sentence, or token **lemma/form** matches headword / variant.
3. Skip duplicates (case-insensitive).
4. Score: SNO surface > length 25–100 chars.

---

## Attribution

- Register entries in `data/corpus/sources.json`
- Applied entries get note: `UD_Naija-NSC example (CC BY-SA 4.0)`
- See `docs/citation-pack.md` for BibTeX

---

## Share-alike

If you redistribute **derivative** example bundles publicly, comply with CC BY-SA 4.0 on UD-sourced sentences.
