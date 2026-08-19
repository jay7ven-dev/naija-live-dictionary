# Phase 1 — Dictionary Entry Schema

**Status:** Defined (2026-07-10)  
**Authority:** IFRA/NLA Standard Naijá Orthography (SNO) — see D1/D2 in `PROJECT.md`  
**Machine schema:** `schema/entry.schema.json`  
**Examples:** `data/examples/entries.json`  
**Validator:** `python schema/validate.py`

---

## Purpose

One entry shape for seed vocabulary (Phase 2), variant collection (Phase 3), and search UI (Phase 4). Headword lookup uses `standard_spelling`; variant→standard lookup indexes `informal_variants[]`.

---

## Entry fields

| Field | Required | Type | Rule |
|-------|----------|------|------|
| `id` | yes | string | Stable slug (`pikin`, `sharp-sharp`). Lowercase, hyphenated. Used in URLs and storage. |
| `standard_spelling` | yes | string | **SNO headword.** Include acute tone marks when they disambiguate (e.g. `déy`, `Naijá`). |
| `informal_variants` | no | string[] | Alternate spellings for search only. Must not duplicate `standard_spelling`. |
| `part_of_speech` | yes | enum | See list below. Use `phrase` for multi-word lemmas stored as one entry. |
| `definitions` | yes | string[] | ≥1 gloss; most common sense first. |
| `example_sentences` | yes | string[] | ≥1 example; prefer SNO spelling in the example text. |
| `notes` | no | string | Tone pairs, plural pattern, reduplication rule, register, variant source. |
| `pronunciation` | no | string | Optional broad hint — not full IPA required for MVP. |

### `part_of_speech` values

`noun`, `verb`, `adjective`, `adverb`, `interjection`, `particle`, `pronoun`, `determiner`, `preposition`, `conjunction`, `phrase`, `other`

---

## Orthography rules (encoding in entries)

| SNO rule | Schema behavior |
|----------|-----------------|
| Minimal tone marking | Diacritics live in `standard_spelling`; explain pairs in `notes` |
| Plural *dem* | Headword is singular lemma; note `word-dem` in `notes` (e.g. `pikin` → `pikin-dem`) |
| Reduplication (bound) | One word in `standard_spelling` (e.g. `shapshap`); hyphenated social forms in `informal_variants` |
| English loans | SNO form in `standard_spelling` (e.g. `buk`); English spelling in `informal_variants` |
| Compounds | Hyphenated SNO in `standard_spelling` when IFRA §4.2 applies (e.g. `strong-hed`) |

---

## Corpus file format (Phase 2+)

**Default:** `data/dictionary.json` — JSON array of entries.

**Optional later:** JSONL (`data/dictionary.jsonl`) for append-friendly pipelines — one entry per line, same fields.

---

## Lookup behavior (Phase 4)

1. **Standard search** — match `standard_spelling`, `definitions`, `example_sentences`
2. **Variant redirect** — if query matches any `informal_variants[]` value, resolve to parent entry’s `standard_spelling`
3. **Normalize query** — case-fold for ASCII; preserve diacritics when present

Build a variant index at load time: `{variant → id}`.

---

## Example entry

```json
{
  "id": "pikin",
  "standard_spelling": "pikin",
  "informal_variants": ["pekin", "pikinn", "pickin"],
  "part_of_speech": "noun",
  "definitions": ["child"],
  "example_sentences": ["Di pikin-dem de ple fo yad."],
  "notes": "Plural: pikin-dem (IFRA §6.2)."
}
```

---

## Validation

```bash
python schema/validate.py
python schema/validate.py data/dictionary.json
```

---

## Phase 1 exit

- [x] Schema documented (this file)
- [x] JSON Schema for tooling
- [x] Example entries
- [x] Runnable validator

**Next:** Phase 3 — variant collection pipeline.

## Phase 2 (complete)

- **Corpus:** `data/dictionary.json` — **306** seed entries (IFRA SNO)
- **Builder:** `python data/build_seed.py`
- **Validate:** `python schema/validate.py data/dictionary.json`
