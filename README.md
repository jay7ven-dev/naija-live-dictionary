# Naijá Live Dictionary

IFRA/NLA Standard Naijá Orthography (SNO) lexical resource with informal → standard lookup, **Fix spelling** (rules), and Keyman keyboard sources.

**Orthography follows the IFRA/NLA Standard Naijá Orthography (2010). This project is not affiliated with IFRA Nigeria.** See [`docs/citation-pack.md`](docs/citation-pack.md) and [`docs/d4-public-release-licensing.md`](docs/d4-public-release-licensing.md).

## Run locally

```bash
python web/serve.py
```

Opens **Fix spelling** at http://localhost:8765/web/normalize.html  
Dictionary: http://localhost:8765/web/index.html  

**Hosted (static):** https://jay7ven-dev.github.io/naija-live-dictionary/ — Fix spelling + dictionary lookup. Advanced English→Pidgin needs local `python web/serve.py` (no server-side MT on Pages).

Do not open HTML as a `file://` URL — dictionary data will not load.

## What this is

A living SNO lexicon (headwords + curated variants, evidence-triggered growth) plus tools: Fix spelling, optional Advanced English→Pidgin, Keyman. Canonical science write-up: [`docs/manuscripts/naija-live-dictionary.md`](docs/manuscripts/naija-live-dictionary.md). Growth policy: [`docs/live-growth.md`](docs/live-growth.md).

## Checks

```bash
python schema/validate.py data/dictionary.json
python web/verify.py
python data/normalize.py --self-check
python data/normalize.py --eval data/eval/messy_pidgin_sample.jsonl
```

## Public release

Checklist: [`docs/public-release-checklist.md`](docs/public-release-checklist.md)  
License: [`LICENSE`](LICENSE)

Offline Tier A/B zip (no IFRA guide body, no full corpus dumps):

```bash
python data/package_release.py
```

Do **not** add the IFRA Guide PDF or long verbatim guide text to a public remote.
