# For researchers

Derived from the canonical manuscript: [`../manuscripts/naija-live-dictionary.md`](../manuscripts/naija-live-dictionary.md). Prefer that paper for full argumentation and references.

## What this resource is

An IFRA/NLA **Standard Naijá Orthography (SNO)**–grounded lexical inventory with:

- SNO headwords and English glosses
- curated informal → standard variant links
- spoken examples from UD_Naija-NSC (CC BY-SA 4.0) where matched
- optional broad pronunciation hints
- TEI Lex-0 export for interop

It is **not** a finished writing system, **not** a production MT product, and **not** a substitute for IFRA guide republication. The Live Dictionary is the public **lexical resource**; licensed text used for suggestions is **development corpora** only. Part II centers **Fix spelling (rules)**; English→Pidgin is optional Advanced; Keyman (II-5b) covers system typing; TEI/UD/FST are research sidecars [see manuscript §1.2, §3.8].

## Orthography policy (D1/D2)

- Headword field `standard_spelling` = SNO only.
- Naija Guru, English etymology, and social spellings = `informal_variants` only.
- See manuscript §2–3 and `../phase-0-orthography-grounding.md`.

## Cite this project

Use BibTeX in [`../citation-pack.md`](../citation-pack.md). Always cite corpus sources you rely on (NaijaSenti, CENCOS, UD_Naija-NSC).

## Key quantitative claims (snapshot 2026-10-01)

Re-verify before publication (`python web/verify.py`):

| Metric | Typical value |
|--------|----------------|
| Entries | 383 |
| Curated mappings | 104 |
| Index keys | 826 |
| Pronunciation present | 383/383 |

Older Part I prose citing 306/52/629 remains historically correct for the 2026-07 snapshot.

## Licensing

Public redistribution follows [`../d4-public-release-licensing.md`](../d4-public-release-licensing.md): cite IFRA; do not republish the IFRA guide body without permission; respect CC BY-SA for UD-derived examples.

## Reproducibility

See website Layer 4 (`/web/docs/repro/`) or manuscript Appendix A.
