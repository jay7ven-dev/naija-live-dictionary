# Phase II-5b — Keyman keyboard

**Status:** Done (Keyman sources)  
**Spec:** `docs/superpowers/specs/2026-09-27-part-ii-5b-keyman-design.md`

## Delivered

- `ime/keyman/naija_sno/naija_sno.kmn` — QWERTY digraphs (`ch` `gb` `sh` `kp` `zh`) + `'` + vowel → acute
- `naija_sno.kps` — package stub for Keyman Developer
- `naija_sno.wordlist.tsv` — generated from II-5a export
- `data/export_keyman_wordlist.py` — regenerates wordlist
- README + package `readme.txt` — local `.kmp` build instructions

## Not in this phase

- Prebuilt `.kmp` in git (build locally)
- Windows TSF / Android IMS / iOS keyboard apps
- Keyman Developer on CI

## Regenerate / check

```bash
python data/export_ime_lexicon.py
python data/export_keyman_wordlist.py
python data/export_keyman_wordlist.py --self-check
python web/verify.py
```

## Runtime for users

Install [Keyman](https://keyman.com/), open `ime/keyman/naija_sno/` in Keyman Developer, build `.kmp`, install.
