# Phase II-2 — Trained normalizer + compare

**Status:** Implemented (2026-09-23)  
**Spec:** `docs/superpowers/specs/2026-09-22-part-ii-normalizer-design.md`

---

## Model

stdlib **exact lookup + NN vote (Levenshtein ≤ 2)** over curated `(variant → SNO)` pairs only:

- `informal_variants[]` on dictionary entries
- `variant_mappings.json`

Single-token pairs only. No torch/HF. Never writes the lexicon.

| Artifact | Path |
|----------|------|
| Trainer / resolve | `data/normalizer_model.py` |
| Production model (all pairs) | `data/normalizer_model.json` |
| Train fold (for compare) | `data/normalizer_model_trainfold.json` |
| Held-out eval | `data/normalizer_heldout.jsonl` |
| CLI | `data/normalize.py --backend rules\|model` |

## Commands

```bash
python data/normalize.py --train
python data/normalize.py --compare          # rules vs model_fold on held-out
python data/normalize.py --backend model --eval
python data/normalize.py --backend model "Di pickin wan book."
```

## Fairness note

`--compare` scores **model_fold** (train subset only) against held-out variants, so it measures generalization. Production `--backend model` uses **all** curated pairs for exact coverage. Rules still use the full `variant_index` (often near-ceiling on this split). Known SNO targets are not NN-rewritten.

## Latest `--compare` (seed=42)

| Backend | Held-out n | Word acc |
|---------|------------|----------|
| rules | 61 | 0.951 |
| model_fold | 61 | 0.082 |

Production model: `Di pickin wan book.` → `Di pikin wan buk.`
