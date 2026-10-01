# Phase II-4 — Keyboard / IME (web compose assist)

**Status:** **Removed from product** (North Star scope realign 2026-10-01). Historical design: `docs/superpowers/specs/2026-09-27-part-ii-4-keyboard-ime-design.md`.

## What replaced it

| Need | Product path |
|------|----------------|
| System-wide SNO typing | **II-5b Keyman** (`ime/keyman/naija_sno/`) — Done (sources + local `.kmp` recipe) |
| Informal → SNO on the web | **Fix spelling** (`web/normalize.html`, rules) — primary sentence tool |
| Lexicon for IMEs | **II-5a** `data/ime/` export |

`web/compose.js` was deleted; digraph UI is no longer shipped. Native OS/store IME apps remain **II-5c+ deferred**.
