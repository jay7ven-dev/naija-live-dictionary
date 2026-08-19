# Phase 3 — Data Collection Ethics & ToS (D3)

**Status:** Resolved (2026-07-10)  
**Applies to:** Variant collection for Live Dictionary (Phase 3+)  
**Does not replace:** Legal review before large-scale automated collection or public corpus release.

---

## Policy summary

Collect Pidgin text **only from admissible sources**. Map informal spellings to IFRA SNO headwords; **do not** republish full third-party corpora without permission.

| Principle | Rule |
|-----------|------|
| **Source admissibility** | Prefer: (1) project-authored samples, (2) user submissions with consent, (3) publicly licensed text with attribution, (4) manual exports you have rights to use. |
| **Platform ToS** | No automated scraping of Twitter/X, Facebook, Instagram, TikTok, Reddit, etc. unless an official API is used **and** storage/redistribution complies with that platform’s terms. Default: **manual copy** or **licensed dataset**. |
| **PII** | Do not store usernames, handles, phone numbers, or other identifying metadata in the corpus. Strip before saving to `data/corpus/`. |
| **Attribution** | Record source type and license in `data/corpus/sources.json` for every file. |
| **Minimization** | Store **tokens/variants** and short example snippets (≤1 sentence), not full threads or articles, unless the source license allows full text. |
| **Human review** | Auto-extracted variant candidates require review before merge into `data/dictionary.json`. |
| **Opt-out** | Remove any submitted sample on request; keep a `removed` flag in manifest if audit trail is needed. |

---

## Admissible source types (ranked)

1. **Project samples** — `data/corpus/samples/*` written for this project (no ToS constraint).
2. **Contributor submissions** — explicit consent to use spelling variants for dictionary research; no PII.
3. **Published literature / news** — excerpt only; cite author/publication; confirm redistribution rights for stored snippets.
4. **Competitive dictionaries (reference only)** — Naijalingo, Glosbe, Naija Guru: use for **variant spelling ideas**, not bulk copying of definitions. Link variants to **our** SNO entries.
5. **API / licensed corpora** — allowed only after documenting API terms in `sources.json` (future).

---

## Not admissible (without separate legal/API review)

- Bulk scraping of social timelines, comment sections, or DMs
- Circumventing login walls or robots.txt
- Storing children’s identifiable content
- Republishing IFRA guide full text in the public dictionary (see D4)

---

## Workflow gate

Before adding a new corpus file:

1. Add row to `data/corpus/sources.json` (`id`, `path`, `source_type`, `license`, `notes`).
2. Run `python data/collect_variants.py extract`.
3. Curate `data/variant_mappings.json` (human-approved variant → entry `id`).
4. Run `python data/collect_variants.py apply` then `python schema/validate.py data/dictionary.json`.

---

## D3 decision (recorded)

**Chosen approach:** Manual-first collection with documented sources, candidate review queue, and no social scraping in Phase 3. Automated ingestion deferred until API/terms are documented per source.
