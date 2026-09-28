# Naijá Live Dictionary

IFRA/NLA Standard Naijá Orthography (SNO) reference with informal → standard lookup.

**Orthography follows the IFRA/NLA Standard Naijá Orthography (2010). This project is not affiliated with IFRA Nigeria.** See [`docs/citation-pack.md`](docs/citation-pack.md) and [`docs/d4-public-release-licensing.md`](docs/d4-public-release-licensing.md).

## Run locally

```bash
python web/serve.py
```

Open http://localhost:8765/web/

Do not open `web/index.html` as a `file://` URL — dictionary data will not load.

## What this is

A structured Live Dictionary: SNO headwords, variants, short examples, pronunciation hints, and a local search UI. Canonical science write-up: [`docs/manuscripts/naija-live-dictionary.md`](docs/manuscripts/naija-live-dictionary.md).

## Checks

```bash
python schema/validate.py data/dictionary.json
python web/verify.py
```

## Public release

Checklist: [`docs/public-release-checklist.md`](docs/public-release-checklist.md)  
License: [`LICENSE`](LICENSE)

Offline Tier A/B zip (no IFRA guide body, no full corpus dumps):

```bash
python data/package_release.py
```

Do **not** add the IFRA Guide PDF or long verbatim guide text to a public remote.
