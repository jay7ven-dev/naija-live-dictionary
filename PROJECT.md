# Pidgin Writing System — Project Planning Document

**Document role:** Authoritative planning document (Strategy A: execution-first)  
**Last updated:** 2026-09-23  
**Status:** Part I complete. Part II normalizer II-1–II-3 landed (harden + local EN→Pidgin translate).

---

# PART I — EXECUTION TARGET (authoritative now)

## 1. Problem & Context

### Introduction

The writing systems adopted all around the world may be distinguished along the major dichotomy of ideographic and alphabetic writing systems. In ideographic writing systems, symbols correspond to the meaning of words. Naijá (previously known as Nigerian Pidgin) is a language that originated from the 15th-century trade contact between the peoples of the Niger Delta and Europeans (xx2).

It is spoken by tens of millions of people across Nigeria and the diaspora, but it remains, functionally, an oral language. It has no state-backed, widely adopted orthography. Historically writing attempts date back to the late 18th century, but the language is still considered "young" in written form and is actively going through orthographic standardization and normalization.

### Limitations

The main issue was that Nigerian Pidgin lacks a standard writing system. I do not think there are keyboards or keypad dictionaries that fully incorporate Pidgin or broken English into their systems. So many advancements with languages being incorporated into the modern-day system of communication.

Here's Naijalingo (crowdsourced slang, informal spellings), Glosbe (auto-generated, thin), and Pidginary (launched Sept 2025 — polished UI, but not orthography-driven). Naija Guru already runs a small dictionary too, but none of these are explicitly built on the IFRA/NLA harmonized orthography as their spelling backbone — that's the actual gap your mini-project could fill.

### Gaps Addressed

No existing resource builds a living, structured dictionary/corpus explicitly anchored to the IFRA/NLA harmonized orthography guidelines in a form that's usable both by humans (as a reference) and by downstream tools/models (as structured data).

---

## 2. Aim & Hypothesis

**Aim:** To reduce the gap between prescriptive Nigerian Pidgin orthography (as defined by linguists/the NLA) and actual user writing practice, by building a living reference (dictionary/corpus) and tools that make the standard easy to use and easy to check against.

**Hypothesis:** If a structured, searchable, IFRA/NLA-grounded dictionary and corpus exist in an accessible digital form, adoption of standardized Pidgin spelling will increase — because previous standardization attempts failed largely due to lack of accessible tooling and documentation, not lack of linguistic merit.

---

## 3. Active Milestone — Live Dictionary (Mini-Project)

Before attempting the full writing-system project, the immediate mini-project is:

**Build a "Live Dictionary" of Nigerian Pidgin, grounded in IFRA/NLA guidelines**

A structured, growing reference containing:

- Words (with IFRA/NLA-standard spelling)
- Phrases
- Example sentences
- Alternate/informal spelling variants (mapped to the standard form — this is what makes it "live" and useful for the later NLP layer)
- Pronunciation guidance where feasible

---

## 4. Scope (Current Increment)

**In scope:**

- Compiling core vocabulary using the IFRA Guide to Standard Naijá Orthography as the spelling authority.
- Structuring entries as: `{standard_spelling, informal_variants[], part_of_speech, definition(s), example_sentence(s), notes}`
- A simple, searchable interface (web-based is reasonable) to browse/search entries.
- A basic data collection pipeline for gathering real Pidgin text samples (social media, informal publishing) to identify common variant spellings.

**Out of scope (this increment):** keyboard input, autocorrect, NLP model training — see Part II North Star.

---

## 5. Exit Criteria (Milestone Definition of Done)

| # | Criterion | Tied to |
|---|-----------|---------|
| 1 | Orthography authority decision recorded (IFRA/NLA vs. Naija Guru reconciliation policy) | Decision Register D1 |
| 2 | Dictionary entry schema defined and documented | Phase 1 |
| 3 | Seed core vocabulary populated (target: few hundred entries per Phase 2) | Phase 2 |
| 4 | Variant-mapping pipeline documented; informal variants linked to standard entries | Phase 3 |
| 5 | Data collection ethics/ToS approach documented | Decision Register D3 |
| 6 | Searchable web interface live (browse + search + variant→standard lookup) | Phase 4 |

**Milestone gate:** All six criteria met → increment complete; North Star phases may begin planning.

---

## 6. Implementation Roadmap (Phases 0–4)

| Phase | Name | Deliverable |
|-------|------|-------------|
| **0** | Literature/orthography grounding | Read IFRA Guide + Naija Guru Standard NP; document agreement/conflict |
| **1** | Data model design | Dictionary entry schema (Section 5 deliverable for agents) |
| **2** | Seed the dictionary | Initial core vocabulary (few hundred entries), standard-applied |
| **3** | Data collection | Real-world Pidgin text samples; map informal variants to standard entries |
| **4** | Build the "live" interface | Searchable dictionary with variant-to-standard lookup |

---

## 7. Decision Register

| ID | Decision | Status | Blocks |
|----|----------|--------|--------|
| **D1** | Primary orthography authority: IFRA/NLA (2009) vs. Naija Guru Standard NP (2024) — reconcile or pick one | **RESOLVED** — IFRA/NLA Standard Naijá Orthography (SNO, 2010 guide) | — |
| **D2** | Single source of truth policy for conflicting rules | **RESOLVED** — SNO governs `standard_spelling`; Naija Guru, English-etymology, and informal forms map as variants | — |
| **D3** | Data collection ethics / platform ToS approach | **RESOLVED** — manual-first; documented in `docs/phase-3-data-collection-ethics.md`; no social scraping in Phase 3 | — |
| **D4** | Licensing/IP for IFRA guide content in public dictionary | **RESOLVED** — tiered release policy; SNO headwords + project content public OK; IFRA guide body not redistributed without permission (`docs/d4-public-release-licensing.md`) | — |

### Program-Level Risks (execution-relevant)

- **Adoption risk:** Prior orthographies failed to spread due to complexity/lack of tooling — design for simplicity from day one.
- **Scope creep:** The three-layer long-term vision is large; discipline needed to keep current increment bounded to dictionary/data layer only.

---

## 8. Execution Handoff (Agent Instructions)

1. Read the IFRA Guide and Naija Guru orthography materials directly before designing the data schema.
2. Propose the dictionary entry schema as a first deliverable.
3. Flag early if IFRA/NLA and Naija Guru rules conflict in ways that block a "single source of truth" decision — surface it rather than silently picking one.
4. Use **brainstorming** before schema, D1, UI, or pipeline design. For web/UI work, read `docs/design-ui-resources.md` and select the skill or resource that matches the task and Part I direction. Do not install uninstalled catalog items unless approved. No design-taste skill is attached to this project.

---

## 9. References (Execution)

- IFRA Nigeria — Guide to Standard Naijá Orthography (NLA harmonized writing system)
- Naija Guru — How to Write Nigerian Pidgin / Standard NP orthography project
- Ofulue & Esizimetor (2010) — history of Pidgin writing attempts
- Deuber & Hinrichs (2007) — Dynamics of orthographic standardization in Jamaican Creole and Nigerian Pidgin
- Mensah et al. (2021) — working orthography proposal for Nigerian Pidgin
- Existing dictionaries (competitive reference): Naijalingo, Glosbe, Pidginary, Naija Guru Dictionary
- https://www.sciencedirect.com/science/chapter/referencework/pii/B0080430767030217
- IFRA Nigeria - GUIDE TO STANDARD NAIJÁ ORTHOGRAPHY. An NLA Harmonized Writing System for Common Naijá Publications

---

# PART II — NORTH STAR (active: normalizer)

> Part I exit criteria met. **Sentence UX (Option B):** English → Pidgin (Marian + SNO) is primary; spelling-fix is secondary. Live Dictionary unchanged. Spec trail: `docs/superpowers/specs/2026-09-22-part-ii-normalizer-design.md`, `…/2026-09-23-part-ii-3-translate-harden-design.md`. Keyboard layouts remain deferred.

## 10. Program Vision — Main Goal

1. **Orthographic standard** — a clear, usable spelling/writing standard, grounded in the existing IFRA/NLA guidelines (not invented from scratch, but operationalized and made practical).

2. **Digital tooling** — keyboard input support, autocorrect/spelling suggestions, and conversion tools (e.g. informal-spelling → standard-spelling normalization).

3. **Data & NLP layer** — a structured corpus and/or model that can recognize, normalize, and work with the natural variation in how people actually write Pidgin today, bridging the "expert vs. user" gap rather than ignoring it.

**Relationship to active milestone:** The Live Dictionary delivers the reference/corpus foundation for Pillar 1 (partial) and Pillar 3 (data layer seed). Phase II-1 operationalizes Pillar 2 (rule-based); Phase II-2 adds Pillar 3 model compare.

---

## 11. Extended Roadmap (Phase 5+ / Part II)

| Phase | Name | Status |
|-------|------|--------|
| **II-1** | Rule-based sentence normalizer (CLI + thin web) | **Done** — `docs/phase-ii-1-normalizer.md` |
| **II-2** | Trained normalizer + eval vs rules | **Done** — `docs/phase-ii-2-normalizer-model.md` |
| **II-3** | Harden fold + local EN→Pidgin translate | **Done** — `docs/phase-ii-3-translate-harden.md` |
| **5 legacy seeds** | Fuzzy, Lin suggest, G2P, FST, TEI | Done (5a–5c); consumed by II-1 |
| **II-4** | Keyboard / IME (web compose assist first) | **Done** — `docs/phase-ii-4-keyboard-ime.md` · spec `docs/superpowers/specs/2026-09-27-part-ii-4-keyboard-ime-design.md` |
| **II-5+** | OS / mobile IME packaging | Deferred (after II-4) |

**Future reference:** arXiv paper — Modeling Orthographic Variation Improves NLP Performance for Nigerian Pidgin (2024) — relevant for II-2.

---

## 12. References (Program)

- arXiv: Modeling Orthographic Variation Improves NLP Performance for Nigerian Pidgin (2024)
- All execution references in Section 9 (shared corpus)
