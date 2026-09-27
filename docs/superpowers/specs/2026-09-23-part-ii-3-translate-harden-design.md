# Part II-3 — Harden orthographic model + EN→Pidgin translate (local)

**Approved:** Approach A. **Date:** 2026-09-23  
**II-3 status:** Implemented 2026-09-23 — see `docs/phase-ii-3-translate-harden.md`.  
**Prior:** II-1 rules normalizer · II-2 thin model (`docs/superpowers/specs/2026-09-22-part-ii-normalizer-design.md`)

## Locked decisions

| Choice | Value |
|--------|--------|
| Sequence | Harden model first (II-3a), then local MT button (II-3b) |
| MT target | True sentence EN→Pidgin (not gloss-swap) |
| Runtime | Local open model (no API keys) |
| Default MT | `NITHUB-AI/marian-mt-bbc-en-pcm` (Hugging Face Marian) |
| Post-process | **Translate → rules normalize** in one click |
| Lexicon | Never auto-write `dictionary.json` / mappings |

## Goal

1. Raise held-out **model_fold** word accuracy above the ~8% baseline with stdlib (or minimal) methods.  
2. Add one-click **English → Pidgin (SNO-normalized)** via local Marian + existing rules normalizer.

---

## Phase II-3a — Harden orthographic model

### In

1. Keep exact lookup + SNO-target guard (do not NN-corrupt known headwords).
2. Add **learned substring/edit rules** from train `(src→tgt)` pairs (Lin-style / frequent char replacements), applied only when exact miss.
3. Keep NN vote as last resort (optional; tighten if it hurts).
4. `--train` regenerates production model + trainfold + heldout.
5. `--compare` reports rules vs model_fold; document new metrics in phase note.
6. Success bar: model_fold word_acc **≥ 0.25** on same seed/split (or document why not reachable without neural MT for variants).

### Out

torch for the orthographic fold; auto-lexicon writes.

### Check

```bash
python data/normalize.py --train
python data/normalize.py --compare
python data/normalize.py --self-check
```

---

## Phase II-3b — Local EN→Pidgin + one-click

### In

1. **CLI:** `python data/translate_en_pcm.py "How are you?"`  
   - Load Marian (download once into HF cache).  
   - Emit raw pcm + SNO-normalized string (rules backend).  
   - Graceful error if optional deps missing.
2. **Optional deps:** extend `requirements-optional.txt` with `transformers`, `torch` (CPU ok), `sentencepiece` as needed. Not required for dictionary/normalize rules.
3. **Web:** on `web/normalize.html`, add button **Translate to Pidgin** (same textarea).  
   - Static JS cannot run Marian; options (pick one in impl, prefer smallest):  
     - **P1 (recommended):** small local endpoint on `web/serve.py` (`POST /api/translate`) calling the Python translator; or  
     - **P2:** document “CLI only” and a note in UI until endpoint exists.  
   - **Implement P1** unless blocked — user asked for one-click in browser.
4. Pipeline: `en_text → marian → pcm_raw → normalize(rules) → show normalized` (optionally show raw in status/detail).
5. Disclaimer: MT output is not IFRA authority until normalized; model may be Bible/BBC-skewed.
6. Phase note + `PROJECT.md` roadmap row.

### Out

Cloud LLM; gloss-only fake translation as the product; training our own Marian from scratch this increment.

### Check

```bash
pip install -r requirements-optional.txt   # once
python data/translate_en_pcm.py "I want a book."
python web/serve.py
# Browser: paste English → Translate to Pidgin → SNO-ish output
```

---

## UI note

Reuse existing normalize page patterns (`docs/design-ui-resources.md`: preserve Live Dictionary chrome; no new design system). Primary skill: **ponytail** (smallest diff). Brainstorming gate satisfied by this spec.

---

## Implementation order

1. Spec review (this file).  
2. II-3a harden + compare.  
3. II-3b CLI translator.  
4. II-3b `/api/translate` + button.  
5. Docs.

## Spec review gate

**Do not implement until reviewed.** Reply **go** or list edits.
