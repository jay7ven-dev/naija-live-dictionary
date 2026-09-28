# D4 — IFRA Public-Release Licensing Policy

**Status:** RESOLVED (2026-07-10)  
**Decision ID:** D4  
**Blocks:** Public deployment / open redistribution of full dictionary bundle

---

## Summary

The Live Dictionary may be **publicly released** under a tiered policy that **cites IFRA/NLA SNO as orthographic authority** without **reproducing the IFRA Guide text**. Project-authored content and properly attributed corpus-derived variant mappings are cleared for release; full IFRA PDF or long verbatim excerpts require separate permission from IFRA Nigeria.

---

## What IFRA SNO is (legal framing)

| Asset | Nature | Our use |
|-------|--------|---------|
| IFRA *Guide to Standard Naijá Orthography* (2010) | Published research/education work (IFRA Nigeria / NLA) | Read as authority for `standard_spelling`; **not** embedded in repo |
| SNO spelling conventions | Linguistic facts + prescriptive standard | Encoded as headwords in `dictionary.json` |
| IFRA web excerpts | Third-party content | Archived locally in `sources/extractions/` for research only |

The guide is publicly described on [IFRA Nigeria’s site](https://ifra-nigeria.org/research/former-projects/89-guide-to-standard-naija-orthography-an-nla-harmonized-writing-system-for-common-naija-publications) but **does not carry an explicit open license** (CC0, CC BY, etc.) on the page. Treat it as **© IFRA Nigeria — all rights reserved** unless IFRA grants written permission.

---

## Release tiers

### Tier A — Public OK (default open-source bundle)

- `data/dictionary.json` — project seed glosses and examples (project-authored)
- `informal_variants[]` — attested spellings from licensed corpora + curated mappings
- `web/` UI, `schema/`, pipeline scripts
- `export/naija-dictionary.lex0.xml` — lexical export with **attribution**
- `docs/citation-pack.md` — bibliography
- Short **fair-use** orthography notes in `notes` (e.g. “Plural: pikin-dem per IFRA §6.2”) — **not** multi-paragraph guide reproduction

**Required notice** (README + web footer):

> Orthography follows the IFRA/NLA Standard Naijá Orthography (2010). This project is not affiliated with IFRA Nigeria. See `docs/citation-pack.md`.

### Tier B — Public with attribution (corpus derivatives)

| Source | License | Allowed |
|--------|---------|---------|
| NaijaSenti pcm | Academic release | Variant tokens + counts; **not** full tweet redistribution in dict entries |
| CENCOS | Zenodo open | Variant mining; cite Agbo & Plag 2022 |
| UD_Naija-NSC | CC BY-SA 4.0 | Example sentences if added; share-alike on derivatives |
| Common Voice pcm | CC0 | Example/pronunciation enrichment |

Register every source in `data/corpus/sources.json`.

### Tier C — Not in public repo without permission

- Full IFRA SNO PDF or HTML mirror
- Long verbatim passages from IFRA guide (> ~90 words continuous)
- Bulk Naija Guru / Naijalingo definitions (ToS unclear)
- Unlicensed social-media scrape dumps

**Action if full IFRA text needed online:** Email IFRA Nigeria (contact via [ifra-nigeria.org](https://ifra-nigeria.org)) requesting republication or CC license for educational dictionary use.

---

## Decision

| Question | Resolution |
|----------|------------|
| Can we publish the dictionary publicly? | **Yes** — Tier A + B with attribution and no IFRA guide body |
| Can we use SNO spellings as headwords? | **Yes** — factual application of a published standard; cite Ofulue & Esizimetor (2010) |
| Can we ship IFRA PDF in repo? | **No** — unless IFRA grants permission |
| Can we quote IFRA rules in docs? | **Minimal** — summary + section refs (as in Phase 0); link to IFRA URL |

---

## Checklist before public release

Operational copy: `docs/public-release-checklist.md`.

- [x] Add `LICENSE` file for project-authored code/data
- [x] Add IFRA/NLA attribution to `web/index.html` footer
- [x] Confirm no IFRA PDF in `sources/` is published to remote (none present; `.gitignore` blocks PDFs)
- [x] Include `docs/citation-pack.md` in release
- [x] Offline Tier A/B zip via `python data/package_release.py` → `dist/`
- [ ] Optional: confirm with IFRA Nigeria in writing for institutional/grant requirements

---

## Related decisions

- **D1/D2:** SNO governs headwords — unchanged  
- **D3:** Manual-first corpus ethics — unchanged  

See also: `docs/phase-3-data-collection-ethics.md`, `docs/citation-pack.md`.
