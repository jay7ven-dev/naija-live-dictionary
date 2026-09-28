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

## Build `.kmp` (local)

```bash
cd ime/keyman/naija_sno
npx --yes @keymanapp/kmc@18 build naija_sno.kmn -o build/naija_sno.kmx
npx --yes @keymanapp/kmc@18 build naija_sno.kps -o build/naija_sno.kmp
```

Output: `ime/keyman/naija_sno/build/naija_sno.kmp` (gitignored). Install with [Keyman](https://keyman.com/).

## Runtime for users

Install Keyman, install the built `.kmp`, enable **Naija SNO**.
