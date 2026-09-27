# Part II-5b — Keyman keyboard (design)

**Status:** Implemented with this increment — see `docs/phase-ii-5b-keyman.md`.  
**Prior:** II-5a IME lexicon export (`data/ime/`) · II-4 web compose assist  
**Orthography authority:** IFRA/NLA SNO (D1)

## Locked decisions

| Choice | Value |
|--------|--------|
| Native IME vehicle | **Keyman** keyboard + wordlist (not Windows TSF / Android / iOS apps) |
| Sources path | `ime/keyman/naija_sno/` |
| Lexicon input | II-5a `data/ime/naija-ime-lexicon.json` (regenerate wordlist after growth) |
| Dictionary writes | Never — Keyman is a consumer only |
| Digraphs | Sequential: `gb` `kp` `sh` `ch` `zh` |
| Acute | `'` + `a/e/i/o/u` → `á/é/í/ó/ú` |
| `.kmp` binary | Built locally in Keyman Developer — not required in git |

## Goal

1. System-wide SNO digraph / tone compose via Keyman on platforms Keyman supports.  
2. Predictive wordlist aligned with the Live Dictionary export.  
3. Keep the repo free of heavy native SDK projects.

---

## In

1. `naija_sno.kmn` — digraph + acute rules on QWERTY.  
2. `naija_sno.kps` — package stub for Keyman Developer.  
3. `data/export_keyman_wordlist.py` → `naija_sno.wordlist.tsv`.  
4. READMEs + phase note + `PROJECT.md` II-5b Done.  
5. Light verify that sources + wordlist exist.

## Out

TSF / Android IMS / iOS keyboard extensions; Keyman Cloud store publish; CI that requires Keyman Developer.

## Check

```bash
python data/export_ime_lexicon.py
python data/export_keyman_wordlist.py
python data/export_keyman_wordlist.py --self-check
python web/verify.py
# Local: open ime/keyman/naija_sno/ in Keyman Developer → Build .kmp → Install
```

## Spec review gate

**Approved by plan choice** (Keyman, 2026-09-27).
