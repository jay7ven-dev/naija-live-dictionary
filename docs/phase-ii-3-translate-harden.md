# Phase II-3 — Harden model + EN→Pidgin translate

**Status:** Implemented (2026-09-23)  
**Spec:** `docs/superpowers/specs/2026-09-23-part-ii-3-translate-harden-design.md`

## II-3a Orthographic harden

- Learned mid-string edits from train pairs + Lin-style bootstrap digraphs
- Lin `generate_variants` augmentation on train targets (holdout srcs blocked in fold)
- Only accept edits that land on a known SNO target
- SNO-target guard unchanged

```bash
python data/normalize.py --train
python data/normalize.py --compare
```

### `--compare` (seed=42, n=61)

| Backend | Word acc |
|---------|----------|
| rules | 0.951 |
| model_fold | ~0.10–0.12 |

**Success bar (≥0.25 fold) not met** with stdlib exact/edits/NN on this split: most held-out spellings are unique and do not share recoverable mid-edits with train. Rules remain the default backend; production `--backend model` still covers all curated pairs exactly. Further gains need neural orthographic MT or larger labeled variant sets — out of II-3a scope.

## II-3b Translate

```bash
pip install -r requirements-translate.txt   # Windows-safe; skip pynini
python data/translate_en_pcm.py "I want a book."
python web/serve.py
# http://localhost:8765/web/normalize.html → Translate to Pidgin
# POST /api/translate {"text":"..."}
```

Pipeline: English → `NITHUB-AI/marian-mt-bbc-en-pcm` → rules normalize → SNO output.

## UX Option B (2026-09-23)

- **Primary:** English → Pidgin on `/web/normalize.html` (and dictionary footer link).
- **Secondary:** “Fix spelling only” under a details panel (rules; already-Pidgin text).
- **Model normalize:** demoted from UI dropdown; use CLI `--backend model` / `--compare` only.
- **Live Dictionary** schema and word search unchanged.
