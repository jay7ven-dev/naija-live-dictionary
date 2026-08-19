# Public-release checklist

**Policy:** [`d4-public-release-licensing.md`](d4-public-release-licensing.md) (D4)  
**Ethics:** [`phase-3-data-collection-ethics.md`](phase-3-data-collection-ethics.md) (D3)  
**Checked:** 2026-08-18

Required notice (README + footer):

> Orthography follows the IFRA/NLA Standard Naijá Orthography (2010). This project is not affiliated with IFRA Nigeria. See `docs/citation-pack.md`.

## D4 items

| Item | Status |
|------|--------|
| `LICENSE` for project-authored code/data | **Done** — mixed notice (MIT code; project data; UD CC BY-SA on example sentences) |
| IFRA/NLA attribution on `web/index.html` footer | **Done** |
| Same notice in `README.md` | **Done** |
| `docs/citation-pack.md` in the tree | **Done** |
| No IFRA PDF in `sources/` | **Pass** — none present; `.gitignore` blocks `*.pdf` / `ifra-guide.pdf` |
| IFRA web extract is short notes, not guide body | **Pass** — `sources/extractions/ifra-sno-web.txt` is a principle list |
| Optional written OK from IFRA Nigeria | **Not done** — only if a grant/institution requires it |

## Do not put on a public remote

| Path / class | Why |
|--------------|-----|
| IFRA Guide PDF or HTML mirror | D4 Tier C |
| Continuous IFRA quotes over ~90 words | D4 Tier C |
| Bulk Naija Guru / Naijalingo definitions | ToS unclear |
| Unlicensed social scrapes | D3 |
| `data/corpus/external/*.conllu` | Full UD treebank; gitignored — ingest locally |
| `data/corpus/external/cencos-transcripts.txt` | Full third-party dump; gitignored — cite Zenodo |

Local copies of ignored corpora may stay on disk for pipelines. Re-fetch with `python data/enrich_examples.py ingest` (UD) and the CENCOS ingest path.

## Before first `git push`

1. Confirm `.gitignore` is committed.
2. `git status` — no `.pdf`, no `pcm_nsc-ud-*.conllu`, no `cencos-transcripts.txt`.
3. Footer/README still carry the IFRA disclaimer.
4. You choose when to commit and push; this checklist does not push for you.

## Optional later

- Ask IFRA Nigeria for educational republication / CC terms (only if you need the guide body online).
- Dual-license SPDX in GitHub repo settings to match `LICENSE` (do not claim a single license for UD sentences).
