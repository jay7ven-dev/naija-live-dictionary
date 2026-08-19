# Live Dictionary UI — quieter + GOV.UK search

**Approved:** A (impeccable then GOV.UK). **Date:** 2026-08-18  
**Surface:** `web/index.html`, `web/style.css`, `web/app.js`  
**Not in this pass:** `web/docs/**` em-dashes, new search engines, accessible-autocomplete npm.

## Evidence

- Assessment A: silent search, 40-card idle, cream/card/stripe tells, nine-link footer.
- Assessment B: `index.html` detector-clean; `style.css:119` `side-tab`; docs em-dashes out of scope.

## In

1. Visible search label; placeholder contrast via `--muted`.
2. Idle = how-to + optional “Browse first 40”; not a catalog dump.
3. Suggestions after **3** characters, **cap 5**, **in-flow** list (pushes results down; no overlay). Prefix on headword/variant. Select fills the field and searches.
4. Drop `.examples` left stripe. Cooler canvas (brand hue, not cream). Footer: Docs, User Guide, disclaimer only.
5. `:focus-visible` on field and list options; `aria-busy` while JSON loads.

## Out

Rewrite, React, uFuzzy/Fuse, Typesense, Stitch DESIGN.md, docs-layer copy.

## Check

`python web/verify.py`  
Browser: `pickin` still banners to `pikin`; empty field shows idle not 40 cards; 3+ letters show ≤5 in-flow options.
