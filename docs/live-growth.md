# Live lexicon growth (evidence-triggered)

**Status:** North Star realign (2026-10-01)

## Rule

Growth is part of “live” (variants↔SNO **plus** ongoing coverage). There is **no calendar quota**.

1. Candidates may be proposed automatically (suggestions queue, licensed development corpora, Lin, etc.).
2. A human **gates** every commit to `dictionary.json` / variant mappings (D3 manual-first).
3. Grow when the queue (or real misses) warrants review — not empty scheduled batches.
4. On each apply, update `data/last_grown.json` (date + counts). UI shows “Lexicon last grown …”.
5. On each apply, regenerate IME + Keyman wordlist exports (`data/export_ime_lexicon.py`, `data/export_keyman_wordlist.py`). Rebuild/reinstall `.kmp` only when asked.

## Coverage sample

Frozen messy-Pidgin set: `data/eval/messy_pidgin_sample.jsonl`  
Baseline: `data/eval/coverage_baseline.json`  

```bash
python data/normalize.py --eval data/eval/messy_pidgin_sample.jsonl
```
