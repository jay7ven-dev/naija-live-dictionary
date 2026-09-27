# Part II — Sentence Normalizer (rules v1 → model compare)

**Approved:** Path C (rules then model); surface 3 (CLI + thin UI); unit 2 (full sentence, token lookup). **Date:** 2026-09-22  
**Pillars:** 2 (autocorrect/normalizer) + 3 (NLP/models)  
**II-1 status:** Implemented 2026-09-23 — `docs/phase-ii-1-normalizer.md`.  
**II-2 status:** Implemented 2026-09-23 — `docs/phase-ii-2-normalizer-model.md`.  
**Authority unchanged:** IFRA/NLA SNO headwords; human gate for lexicon writes.

## Goal

Ship a **sentence-level orthographic normalizer** that maps informal Pidgin tokens to SNO forms using Live Dictionary assets, then train a thin model on curated pairs and **compare** against the rule baseline.

## Decisions (locked)

| Choice | Value |
|--------|--------|
| Sequence | Rule-based v1 first; trained backend second |
| Surface | Shared core → CLI first → thin web page/section |
| Unit | Full sentence; per-token lookup; keep punctuation/spacing |
| Lexicon writes | Never auto-apply model or fuzzy hits into `dictionary.json` |

## Approach

Reuse existing lookup stack (`variant_index.json` exact → `fuzzy_lookup.json` Levenshtein ≤ 2 → resolve to `standard_spelling`). Prefer this over a new NLP platform (YAGNI). Model later = supervised edits from human-approved `(variant → SNO)` only.

---

## Phase II-1 — Rule-based normalizer (v1)

### In

1. **Core** (`data/normalize.py` or equivalent): tokenize on whitespace; peel/reattach simple punctuation; for each token: exact index → fuzzy ≤2 → else leave + mark `unknown`. Map entry ids to `standard_spelling` via `dictionary.json`.
2. **CLI:** `python data/normalize.py "…"` → normalized sentence; optional `--json` for per-token decisions (`input`, `output`, `method`: exact|fuzzy|unknown|identity).
3. **Web:** one Normalize paste box (same indexes/rules as CLI; static JS, no new backend). Link from Live Dictionary UI without redesigning search.
4. **Gold check:** small fixture of input sentences → expected SNO strings; one runnable self-check fails if logic regresses.
5. **Docs:** update `PROJECT.md` Part II status to active for this increment; short phase note under `docs/`.

### Out (II-1)

Keyboard layouts; trained models; auto-merge to dictionary; grammar rewrite; social scraping; new heavy deps.

### Check (II-1)

```bash
python schema/validate.py data/dictionary.json
python data/normalize.py --self-check   # or dedicated small test script
python web/verify.py
python web/serve.py   # Normalize page: paste informal sentence → SNO tokens
```

---

## Phase II-2 — Trained normalizer (compare)

### In

1. **Supervision:** curated `variant_mappings` + entry `informal_variants` → `(src, tgt)` pairs only. No raw corpus auto-labels.
2. **Model:** thin char- or token-edit model (stdlib/minimal deps preferred; optional torch/HF only if approved when implementing). Same I/O shape as rules.
3. **CLI/UI switch:** `--backend rules|model` (default `rules`).
4. **Eval:** held-out pairs → word accuracy + sentence exact-match; report rules vs model side by side.
5. **Gate:** model output is suggestion/normalization only; never writes `dictionary.json` / `variant_mappings.json`.

### Out (II-2)

Full ASR; production autocorrect IME; training on unreviewed tweets; replacing the human curation pipeline.

### Check (II-2)

```bash
python data/normalize.py --backend rules --eval path/to/heldout.jsonl
python data/normalize.py --backend model --eval path/to/heldout.jsonl
# Compare printed metrics; rules remain default
```

---

## Data flow

```
sentence
  → tokenize (+ keep punct)
  → per token: variant_index → fuzzy_lookup → standard_spelling | unknown
  → reassemble sentence
  → CLI / web

(later) same tokens → model backend → same assemble + eval vs rules
```

## Risk notes

- English code-switch tokens will often stay `unknown` (correct for v1).
- Fuzzy ≤2 can false-positive; expose method in JSON so UI can flag fuzzy hits.
- Re-running `build_seed.py` still overwrites headwords; normalizer must not depend on mutating seed.

## Implementation order

1. Write/land this spec (done when reviewed).  
2. II-1 core + CLI + self-check.  
3. II-1 thin web Normalize UI.  
4. Update Part II / phase docs.  
5. Stop for review → II-2 train + eval only after II-1 accepted.

## Spec review gate

**Do not implement until this file is reviewed.** Reply to confirm or list edits.
