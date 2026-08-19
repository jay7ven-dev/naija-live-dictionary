# Phase 0 — Orthography Grounding

**Status:** Initial synthesis (web sources read; full IFRA PDF not yet archived locally)  
**Deliverable:** Agreement/conflict matrix to inform Decision Register D1 and D2  
**Sources consulted:**

| Source | URL | Year |
|--------|-----|------|
| IFRA / NLA — Guide to Standard Naijá Orthography (SNO) | https://ifra-nigeria.org/research/former-projects/89-guide-to-standard-naija-orthography-an-nla-harmonized-writing-system-for-common-naija-publications | 2010 |
| Naija Guru — Standard NP (English) | https://naija.guru/en/grammar/how-to-write-nigerian-pidgin/ | 2024 |
| Naija Guru — Standard NP (community summary) | https://community.naija.guru/t/the-standard-np-orthography/22 | 2024 |

**Next extraction step:** Run `article-extractor` / `learn-this` on URLs above; archive under `sources/extractions/`. Obtain IFRA PDF for `skill-seekers` skill generation.

---

## Shared principles (agreement)

Both systems aim at a practical Latin-script orthography for Nigerian Pidgin / Naijá with these overlaps:

| Topic | IFRA / NLA (SNO) | Naija Guru (Standard NP) | Notes |
|-------|------------------|------------------------|-------|
| Script | Latin alphabet + digraphs | Latin alphabet | Compatible |
| Core digraphs | ch, gb, sh, kp, zh | ch, gb, sh, kp used in examples; zh in “measure” | Standard NP docs emphasize English-keyboard pragmatism; digraph set aligns in practice |
| Phonetic intent | “Spelled as pronounced” (common core) | English-friendly but documents IPA consonant/vowel inventory | Same direction; Standard NP leans etymological for many English loans |
| Tone disambiguation | Minimal marking; **high tone only** (acute ´); low unmarked | Minimal marking; **acute only** on “tone words”; low unmarked | **Strong agreement** — critical for dictionary `notes` field |
| Example: progressive vs locative | de (PROG) vs dé (is/are, stay) | dey gym vs déy gym | **Same pattern** |
| Plural with *dem* | Hyphenate: `pikin-dem` | Hyphenate: `man-dem`, `people-dem` | **Agreement** |
| Punctuation | Standard marks (period, comma, etc.) | Standard English punctuation set | Agreement |
| Adoption problem | Prior standards failed without tooling | Explicitly cites complexity + lack of documentation/tooling | Both motivate this Live Dictionary project |

---

## Material differences (conflicts — D1 / D2)

| # | Rule area | IFRA / NLA (SNO) | Naija Guru (Standard NP) | Impact on dictionary |
|---|-----------|------------------|--------------------------|----------------------|
| **C1** | **Reduplication (bound / ideophonic)** | Write **together**: `potopoto`, `chukuchuku`, `moimoi` | Hyphenate most reduplications: `sharp-sharp`, `small-small`, `wuru-wuru` | Variant→standard mapping must pick a policy; informal social media may use either |
| **C2** | **Intensification (free morpheme repeat)** | **Separate words**: `wel wel`, `bad bad`, `koret koret` | Often **hyphenated** reduplication (same hyphen rule as C1) | Ambiguous boundary between “intensification” vs “reduplication” in user text |
| **C3** | **Compounding** | Hyphenate when one word modifies another: `strong-hed`, `akara-wuman` | Hyphenate some compounds: `i-too-know`, `ghana-must-go` | Largely compatible; edge cases need schema `compound_type` or free-text `notes` |
| **C4** | **Affixation** | Single word: `woka`, `bois`, `smoka` | English loans often **unchanged** spelling (`book`) | IFRA allows English plural marking as one word (`bois`); Standard NP dictionary may prefer English spellings for loans |
| **C5** | **Vowel merging** | Explicit: e = [e]/[ε], o = [o]/[ɔ] for typing ease | IPA table distinguishes /e/ vs /ε/, /o/ vs /ɔ/ but writing rules don’t mandate sub-dots | PT (phonological transcription) vs SNO — dictionary may need `standard_spelling` vs optional `phonological_form` |
| **C6** | **Authority & goal** | NLA harmonized standard (2009 conference); linguistic/academic lineage | 2024 pragmatic standard “for wide-scale adoption”; tooling-first (Naija Guru) | **D1 core tension** — not purely technical |
| **C7** | **English loan spelling** | Adapt to Naijá sound patterns (`buk`, `lait`, `vidio`) | “Majority spelled the same as English” with exceptions in dictionary | Major source of informal↔standard variant pairs for Live Dictionary |
| **C8** | **Emphatic possessive** | Hyphenate `-im`: `Meri-im mama` | Not highlighted in grammar page | IFRA-specific; optional schema field |

---

## Preliminary D1 options (for brainstorming — not decided)

| Option | Policy | Pros | Cons |
|--------|--------|------|------|
| **A — IFRA-primary** | `standard_spelling` = SNO; map Naija Guru + informal as variants | Matches PROJECT.md spelling authority; academic/NLA lineage | Naija Guru users may see “standard” as divergent from 2024 tooling ecosystem |
| **B — Standard NP-primary** | Standard NP as headword; IFRA as documented alternate | Aligns with active dictionary UX (Pidginary, Naija Guru) | Weakens stated IFRA/NLA grounding in PROJECT.md |
| **C — Dual authority (explicit)** | Every entry records `authority: IFRA \| NP \| both`; conflicts flagged in `notes` | Honest about D1; supports “live” variant mapping | More complex schema and editorial workflow |
| **D — IFRA head + NP compatibility layer** | SNO headword; accept NP hyphenation variants where C1/C2 differ | Ponytail-friendly; preserves IFRA anchor | Requires clear public docs on hyphenation rules |

## D1 decision (recorded 2026-07-10)

**Chosen:** **Option A — IFRA-primary**

- `standard_spelling` = IFRA/NLA Standard Naijá Orthography (SNO)
- Naija Guru Standard NP, English-etymology, and informal/social spellings → `informal_variants[]`
- Conflicts C1–C2 (e.g. `sharp-sharp` → map to SNO `shapshap` or documented IFRA intensification form) handled per SNO rules in `notes` where non-obvious

**D2:** Single source of truth = SNO for all headwords.

---

## Tone-marking reference (shared — high priority for schema)

Both systems use **acute accent only** on disambiguating tone. Dictionary entries should support:

- `standard_spelling` (with diacritics when required)
- `informal_variants[]` (often unmarked tone)
- `notes` explaining tone pairs where minimal marking applies (e.g. de/dé, dey/déy)

IFRA examples: `bába` (barber) vs `baba` (father); `Naijá` vs `Naija` (Niger).

---

## Alphabet inventory (IFRA SNO — baseline)

28 letters: **a, b, ch, d, e, f, g, gb, h, i, j, k, kp, l, m, n, o, p, r, s, sh, t, u, v, w, y, z, zh**

Phonological Transcription (PT) variant uses sub-dots for +/− ATR vowels (ẹ, ọ) for scientific use — out of scope for common dictionary unless `notes` / advanced field.

---

## Phase 0 exit checklist

- [x] IFRA SNO principles summarized from official IFRA page
- [x] Standard NP principles summarized from Naija Guru
- [x] Agreement/conflict matrix drafted (this document)
- [ ] Primary sources archived locally (`sources/extractions/`)
- [ ] IFRA PDF obtained for Skill Seekers orthography skill
- [x] D1 decision recorded — **IFRA/NLA SNO primary** (2026-07-10)
- [x] D2 resolved — SNO governs headwords; other systems are variants
- [ ] Mensah et al. (2021), Deuber & Hinrichs (2007) — secondary cross-check (optional Phase 0 extension)

---

## Handoff to Phase 1

Do **not** finalize entry schema until D1 direction is chosen. Schema must accommodate at minimum:

- `standard_spelling`, `informal_variants[]`, `part_of_speech`, `definition(s)`, `example_sentence(s)`, `notes`
- Conflict rules C1, C2, C7 as first-class variant-mapping concerns
- Optional: `authority`, `tone_note`, `compound_type`

Invoke **brainstorming** skill for D1 + schema design session.
