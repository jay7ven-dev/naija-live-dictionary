# Naijá Live Dictionary: An IFRA/NLA-Grounded Lexical Resource for Orthographic Standardization

**Document type:** Scientific manuscript (project-canonical)  
**Status:** Canonical reference for documentation (snapshot 2026-10-01)  
**Canonical data:** `data/dictionary.json`  
**Orthography authority:** IFRA/NLA Standard Naijá Orthography (SNO) [1]

---

## Abstract

Nigerian Pidgin (Naijá) is widely spoken but lacks a single, widely adopted written standard in everyday digital use. Prior orthographies exist, yet accessible tooling that operationalizes a linguistic standard remains scarce. This paper presents the **Naijá Live Dictionary**, a structured, searchable **lexical resource** whose headwords follow the IFRA/Nigeria Linguistic Association (NLA) Standard Naijá Orthography (SNO) [1]. The system links informal and English-etymology spellings to SNO forms through a human-gated variant pipeline, and exposes lookup via a local web interface. The current release contains **503** validated entries, **104** curated variant mappings, and **1026** indexed lookup keys, with pronunciation hints on most entries. Universal Dependencies (UD) Naija–NSC example enrichment, TEI Lex-0 export, and FST candidate generators are maintained as **research sidecars**, not product claims [5]. Licensed **development corpora** (NaijaSenti [2], CENCOS [3]) inform suggestion generation but do not auto-write dictionary content and are not marketed as a released text corpus. Beyond the Part I dictionary milestone, the repository ships Part II **sentence tools**: a rules-based orthographic normalizer (primary **Fix spelling** UX), an experimental thin spell-mapping model for offline comparison only, optional local English→Pidgin Marian MT under **Advanced**, and a Keyman keyboard (II-5b) for system-wide SNO typing [11], [12]. We document methodology, data sources, validation, and limitations, and position the resource as a reproducible foundation for orthography-aware tools rather than a finished writing system or production MT product.

**Keywords:** Nigerian Pidgin, Naijá, orthography, lexicography, variant mapping, IFRA/NLA SNO, normalization, low-resource languages

---

## 1. Introduction

### 1.1 Motivation

Naijá (also known as Nigerian Pidgin) is used by tens of millions of speakers across Nigeria and the diaspora, yet writing practice remains highly variable [6]. Historical and contemporary standardization efforts have produced linguistic guidance, but adoption has been limited by complexity and by the absence of everyday digital references and tools [1], [6]. Existing online dictionaries and apps (e.g., crowdsourced slang resources, auto-generated bilingual pages, or polished commercial UIs) typically do not treat a published linguistic orthography as the exclusive spelling backbone for headwords.

The gap addressed here is therefore practical as well as linguistic: **a living lexical resource (SNO headwords + curated variant links, with evidence-triggered growth) anchored to IFRA/NLA SNO**, usable by humans for lookup and by machines as structured data. Internal licensed text used for suggestions is termed **development corpora**, not a public corpus product.

### 1.2 Aim and scope

**Aim.** Reduce the gap between *prescriptive* Naijá orthography (as defined in the IFRA/NLA guide) and *observed* user spellings by providing (a) SNO headwords with glosses and examples, (b) explicit informal→standard mappings, and (c) a searchable interface.

**Hypothesis (program-level).** If an accessible, IFRA/NLA-grounded dictionary and variant index exist in digital form, standardized spelling becomes easier to check against and to adopt in tools—addressing tooling and documentation failures more than linguistic merit alone (see project planning document).

**In scope (completed Part I mini-milestone).** Schema design; seed lexicon; ethics-constrained development-corpus ingest; curated variant mapping; local web search with exact and fuzzy tiers; pronunciation hints. TEI Lex-0 export, UD example enrichment, and FST generators exist as research sidecars.

**In scope (Part II sentence tools, landed).** Rules-based sentence orthographic normalizer as **primary Fix spelling** UX; experimental thin spell-mapping model for offline rules-vs-model comparison only; optional local English→Pidgin Marian translation with SNO post-normalize under Advanced; Keyman SNO keyboard (II-5b) and regenerable IME lexicon export (II-5a) [11], [12].

**Out of scope (still deferred).** Production-grade neural orthographic autocorrect (we expose **spelling suggestions** via fuzzy lookup and Keyman wordlist only); claiming MT output as IFRA orthography authority without the SNO post-pass and human review. Native TSF / Android / iOS **apps** (II-5c+) remain deferred. Web compose assist (II-4) was removed from the product surface.

### 1.3 Contributions

1. **Authority policy.** A recorded decision that IFRA/NLA SNO governs all `standard_spelling` values; competing systems (e.g., Naija Guru Standard NP) and informal forms are variants only [1], [7].
2. **Reproducible lexicon schema** with machine validation (`schema/entry.schema.json`).
3. **Human-gated variant pipeline** over licensed corpora, with explicit rejection of English code-switch false positives.
4. **Operational lookup stack:** exact variant index, substring search, and Levenshtein fuzzy suggestions (distance ≤ 2).
5. **Interop and attribution (research):** TEI Lex-0 export, citation pack, and tiered public-release licensing (Decision D4).
6. **Sentence tooling (Part II):** primary Fix spelling (rules) over dictionary assets; optional Advanced EN→PCM MT with SNO post-processing; Keyman keyboard; clear separation from word-level Live Dictionary lookup [11], [12].



---

## 2. Related Work

### 2.1 Orthographic standardization

Ofulue and Esizimetor’s *Guide to Standard Naijá Orthography* (IFRA/NLA, 2010) provides the primary spelling authority used here [1]. Sociolinguistic work on orthographic standardization in Caribbean and West African contact varieties documents the tension between linguistic prescription and popular writing practice [6]. More recent community standards (e.g., Naija Guru Standard NP, 2024) emphasize English-keyboard pragmatism; Phase 0 project analysis records substantial agreement with SNO on digraphs and minimal tone marking, and material conflict on reduplication, intensification spacing, and English-loan spelling [7]. This project resolves conflicts by **IFRA-primary headwords** with alternate forms in `informal_variants`.

### 2.2 Computational resources for Nigerian Pidgin

NaijaSenti provides Twitter-derived sentiment data including Nigerian Pidgin content [2]. CENCOS documents English–Nigerian Pidgin code-switching speech transcripts [3]. The UD Naija–NSC treebank supplies spoken Naijá sentences under CC BY-SA 4.0 [5]. Lin et al. show that modeling orthographic variation improves NLP performance for Nigerian Pidgin [4]; we implement a **subset** of orthographic edit rules as a *suggestion* generator only—never as unsupervised lexicon writes.

### 2.3 Lexicographic and product landscape

Commercial and community dictionaries (Naijalingo, Glosbe, Pidginary, Naija Guru Dictionary) offer useful coverage or UX but are not, as a class, explicitly structured as IFRA/NLA SNO-backed machine-readable headword inventories with a curated informal→standard index. The Live Dictionary targets that niche rather than competing on UI polish alone.

---

## 3. Methodology

### 3.1 Design principles

1. **Single orthographic source of truth** for headwords (SNO).
2. **Human review before merge** of corpus-derived variants (Decision D3 ethics).
3. **Minimization:** store tokens/variants and short examples; do not republish full third-party corpora or IFRA guide body (D3/D4).
4. **JSON as canonical storage**; TEI Lex-0 as one-way export for interop.
5. **Ponytail / YAGNI:** prefer stdlib pipelines and a static local web UI over premature platforms.

### 3.2 Entry model

Each entry is a JSON object validated against `schema/entry.schema.json`. Required fields: `id`, `standard_spelling`, `part_of_speech`, `definitions` (≥1), `example_sentences` (≥1). Optional: `informal_variants`, `notes`, `pronunciation`.

Orthography encoding rules (project schema documentation):

| SNO practice | Encoding |
|--------------|----------|
| Minimal tone marking | Diacritics in `standard_spelling`; pairs explained in `notes` |
| Plural *dem* | Singular lemma as headword; pattern in `notes` |
| Bound reduplication | One word in SNO (e.g. `shapshap`); hyphenated social forms as variants |
| English loans | SNO form as headword (e.g. `buk`); English spelling as variant |

### 3.3 Seed lexicon

A seed builder (`data/build_seed.py`) populates IFRA-aligned core vocabulary. Current size: **503** entries (few-hundred target for Phase 2; live count from `schema/validate.py` / `web/verify.py`).

### 3.4 Variant pipeline

```
Corpus (.txt) → extract → candidates / suggestions
                         → human curate → variant_mappings.json
                         → apply → dictionary.json
                         → index → variant_index.json + fuzzy_lookup.json
```

- **Extract / suggest:** token frequencies from registered corpora; Lin-inspired edits and fuzzy candidates written to `suggestions.json` as **pending_review**.
- **Curate:** human-approved rows in `variant_mappings.json` (batches 1–4 via `curate_mappings.py`). Auto-apply of high-recall fuzzy heuristics was tested and **rolled back** after English code-switch false positives (e.g., `your`→`sour`).
- **Apply / index:** merge variants onto entries; rebuild exact and fuzzy indexes.

Batch policy (simplified):

| Batch | Policy |
|-------|--------|
| 1 | Hand-verified high-confidence mappings |
| 2 | Lin-only, count ≥ 5, forward-validated, English blocklist |
| 3–4 | Manual review of remaining lin/English-loan patterns |

### 3.5 Example enrichment (UD Naija–NSC)

`enrich_examples.py` downloads CoNLL-U splits, prefers `# text_ortho`, matches headwords/lemmas/forms, and applies at most two new examples per entry (cap three total). Attribution note: `UD_Naija-NSC example (CC BY-SA 4.0)`.

### 3.6 Pronunciation and NLP seeds

Rule-based broad G2P hints (`g2p_hints.py` / `enrich_pronunciation.py`) fill optional `pronunciation` fields (not full IPA). Optional Pynini FST rules (`fst_variants.py`) feed **research** suggestion mode with Lin fallback. These do not alter SNO headwords and are not product features.

### 3.7 User interface

A static browser UI (`web/`) loads `dictionary.json`, `variant_index.json`, and `fuzzy_lookup.json` from a local server rooted at the project directory (`web/serve.py`). Lookup order: exact variant index → substring search → fuzzy “Did you mean?” (Levenshtein ≤ 2).

### 3.8 Sentence tools (Part II)

Orthographic **normalize** (`data/normalize.py`, primary **Fix spelling** on `/web/normalize.html`) maps each token via the variant index (exact → fuzzy ≤ 2 → leave unknown). It does **not** rewrite English grammar; English residue on English inputs is expected. An experimental **model** backend (exact curated pairs + edit/NN heuristics) exists for offline `--compare` against rules only; it is not the product UX [11], [12]. A frozen messy-Pidgin coverage sample lives at `data/eval/messy_pidgin_sample.jsonl` with baseline `data/eval/coverage_baseline.json`.

**English → Pidgin** (optional Advanced) runs local Marian MT (`NITHUB-AI/marian-mt-bbc-en-pcm` via optional `transformers`/`torch`) then applies rules normalize for SNO spelling (`data/translate_en_pcm.py`, `POST /api/translate`). MT output is not treated as IFRA authority by itself. II-5a ships a regenerable IME lexicon export under `data/ime/` (refreshed on lexicon growth); II-5b provides Keyman keyboard sources under `ime/keyman/naija_sno/` for system-wide typing (local `.kmp` build). Web compose assist (II-4) is not shipped.

### 3.9 Interoperability (research)

`export/tei_lex0.py` produces `export/naija-dictionary.lex0.xml` from the canonical JSON (one-way research interchange). Citations are maintained in `docs/citation-pack.md`.

---

## 4. Data Sources

All ingested files must be registered in `data/corpus/sources.json` with license notes.

| Source | Role | License / terms | Use in project |
|--------|------|-----------------|----------------|
| IFRA/NLA SNO guide [1] | Orthography authority | Cite; do not republish guide body without permission (D4 Tier C) | Headword policy |
| Project-authored samples | Seed phrases / social-style samples | Project | Training pipeline + examples |
| NaijaSenti pcm [2] | Variant suggestion mining | Academic corpus; cite; do not dump full tweets into entries | Suggestions (partial ingest) |
| CENCOS [3] | Code-switched speech transcripts | Zenodo open; cite Agbo & Plag | Suggestions; high English noise → blocklists |
| UD_Naija-NSC [5] | Spoken example sentences | CC BY-SA 4.0 | Example enrichment (share-alike on derivatives) |
| Mozilla Common Voice pcm | Optional pronunciation/sentence support | CC0 | Optional ingest path |

**Ethics (D3).** No social-platform scraping by default; strip PII; human review before dictionary merge; opt-out for submitted samples.

---

## 5. Validation

### 5.1 Structural validation

```text
python schema/validate.py data/dictionary.json
→ OK: 503 entries validated   # live 2026-10-01; prior snapshot was 473
```

Schema enforces required fields, POS enum, and `additionalProperties: false`.

### 5.2 Lookup smoke tests

```text
python web/verify.py
→ OK: 503 entries, 1026 index keys, 1026 fuzzy terms, web + docs layers present
```

Hard-coded regression lookups include `pickin`→`pikin`, `book`→`buk`, `dey`→`de-copula`. Orthographic normalize self-check: `python data/normalize.py --self-check`.

### 5.3 Example enrichment report

```text
python data/enrich_examples.py report
```

Historical Part I run (2026-07): 8,790 UD sentences parsed; 519 examples applied across 264 entries [8]. Re-run the report before citing live multi-example counts (validators first when numbers conflict).

### 5.4 Quantitative snapshot (live 2026-10-01)

| Metric | Value |
|--------|------:|
| Dictionary entries | 503 |
| Schema-valid | 503/503 |
| Pronunciation present | 503/503 |
| Curated variant mappings | 104 |
| Index / fuzzy terms | 1026 |
| Orthographic normalizer | Rules default; model CLI/`--compare` only |
| EN→Pidgin sentence path | Local Marian + rules SNO post-pass (optional deps) |
| Pending auto-suggestions (uncurated) | large (~1.6k historically); not applied |

### 5.5 Negative validation (lessons)

An early batch-1 auto-heuristic (~124 fuzzy mappings) produced systematic false positives from CENCOS English tokens. The seed was reset and only human-verified lists retained. This failure mode is treated as evidence that **suggestion ≠ lexicon**.

---

## 6. Limitations

1. **Coverage.** 503 entries is a seed, not a comprehensive dictionary of Naijá.
2. **Authority completeness.** Full IFRA PDF is not redistributed; SNO encoding relies on documented principles and web/guide summaries plus editorial judgment [1], [7].
3. **Corpus bias.** CENCOS is code-switched English–Pidgin speech; raw frequency rankings over-represent English function words.
4. **NaijaSenti ingest.** Full tweet-scale ingest may require additional dependencies (`datasets`); current pcm sample may be partial.
5. **Examples.** UD matching is heuristic; orthography in `# text_ortho` may still diverge from SNO; enrichment counts drift—re-run `enrich_examples.py report` before citing.
6. **Pronunciation.** Broad hyphenated hints, not IPA or audio alignment (live seed has hints on all entries).
7. **Evaluation.** No user study yet of adoption; orthographic model fold accuracy remains far below rules on held-out pairs; MT quality is not systematically scored here.
8. **Licensing.** Public release must respect D4 tiers and CC BY-SA share-alike for UD-derived example bundles; third-party Marian weights have their own terms.
9. **Hypothesis untested.** The program claim that tooling increases SNO adoption is motivational, not empirically confirmed here.
10. **Sentence MT ≠ orthography authority.** English→Pidgin changes meaning/structure; only the SNO post-pass and dictionary policy encode IFRA spelling. Spelling-fix alone leaves English residue on English inputs by design.

---

## 7. Discussion

### 7.1 Alignment with initial goals

The Live Dictionary mini-project exit criteria—authority decision, schema, seed lexicon, variant pipeline + ethics, and searchable UI—are met. The resource therefore satisfies the *immediate* Part I aim: an IFRA-grounded living lexical reference with informal→standard lookup. Part II now centers **Fix spelling (rules)** as the primary sentence tool, with optional Advanced EN→Pidgin, Keyman (II-5b) for system typing, and IME lexicon export (II-5a); strong orthographic neural models and native store IMEs (II-5c+) remain open. Separating Fix spelling from MT avoids confusing token SNO mapping with translation.

### 7.2 Design implications

Human gating is not a temporary inconvenience: for code-switched development corpora it is a **correctness requirement**. Lin-style orthographic rules [4] are useful as *candidate generators* when combined with blocklists, forward validation, and low auto-thresholds. Fuzzy search improves UX after exact miss (spelling suggestions) but must not write the lexicon and is not claimed as full autocorrect.

### 7.3 Reproducibility and documentation

Canonical scientific claims in this manuscript should drive developer, researcher, and user documentation. Phase docs under `docs/phase-*.md` remain historical execution logs; when numbers conflict, prefer live validators and this manuscript’s snapshot date. Lexicon growth policy: `docs/live-growth.md`.

### 7.4 Future work

- Expand curated mappings from pending suggestions with continued human review (evidence-triggered).
- Complete licensed development-corpus ingest where technically blocked.
- User studies of lookup success, spelling preference, and sentence-tool usefulness.
- Stronger orthographic models or eval suites (rules still dominate the thin fold baseline).
- Keyboard / IME: native TSF / Android / iOS apps (II-5c+); Keyman sources (II-5b) and lexicon export (II-5a) shipped; web compose (II-4) withdrawn from product.
- Public release packaging under D4 Tier A/B with clear attribution.
- Keep manuscript metrics aligned with live validators after each lexicon growth pass.

---

## Acknowledgments

Orthography follows IFRA/NLA SNO [1]. This project is not affiliated with IFRA Nigeria. Corpora authors and Universal Dependencies contributors are gratefully acknowledged; see citation pack for BibTeX.

---

## References

[1] C. Ofulue and E. Esizimetor, *Guide to Standard Naijá Orthography: An NLA Harmonized Writing System for Common Naijá Publications*. IFRA Nigeria / NLA, 2010.

[2] S. H. Muhammad, D. I. Adelani, et al., “NaijaSenti: A Nigerian Twitter Sentiment Corpus for Multilingual Sentiment Analysis,” in *Proc. LREC*, 2022. [Online]. Available: https://aclanthology.org/2022.lrec-1.63/

[3] M. Agbo and I. Plag, “CENCOS: Corpus of English-Nigerian Pidgin Code-Switching,” Zenodo, 2022, doi: 10.5281/zenodo.7314016.

[4] Y. Lin et al., “Modeling Orthographic Variation Improves NLP Performance for Nigerian Pidgin,” in *Proc. LREC-COLING*, 2024. [Online]. Available: https://aclanthology.org/2024.lrec-main.1006/

[5] B. Caron et al., “Naija Treebank (UD_Naija-NSC),” Universal Dependencies, 2020, CC BY-SA 4.0. [Online]. Available: https://github.com/UniversalDependencies/UD_Naija-NSC

[6] D. Deuber and L. Hinrichs, “Dynamics of Orthographic Standardization in Jamaican Creole and Nigerian Pidgin,” *English World-Wide*, 2007, doi: 10.1111/j.1467-971X.2007.00486.x.

[7] Naijá Live Dictionary project, “Phase 0 — Orthography Grounding,” internal project documentation, 2026. (`docs/phase-0-orthography-grounding.md`)

[8] Naijá Live Dictionary project, “Phase R4 — UD_Naija-NSC Example Enrichment,” internal project documentation, 2026. (`docs/phase-r4-ud-examples.md`)

[9] Naijá Live Dictionary project, “Citation Pack,” 2026. (`docs/citation-pack.md`)

[10] Naijá Live Dictionary project, “D4 — IFRA Public-Release Licensing Policy,” 2026. (`docs/d4-public-release-licensing.md`)

[11] Naijá Live Dictionary project, “Part II — Sentence Normalizer (rules → model compare),” design + phase notes, 2026. (`docs/superpowers/specs/2026-09-22-part-ii-normalizer-design.md`, `docs/phase-ii-1-normalizer.md`, `docs/phase-ii-2-normalizer-model.md`)

[12] Naijá Live Dictionary project, “Part II-3 — Harden + EN→Pidgin translate (Option B UX),” 2026. (`docs/superpowers/specs/2026-09-23-part-ii-3-translate-harden-design.md`, `docs/phase-ii-3-translate-harden.md`)

---

## Appendix A — Reproducibility commands

```bash
python schema/validate.py data/dictionary.json
python web/verify.py
python data/normalize.py --self-check
python data/enrich_examples.py report
python export/tei_lex0.py
python web/serve.py   # http://localhost:8765/web/  ·  /web/normalize.html
# optional MT:
# pip install -r requirements-translate.txt
# python data/translate_en_pcm.py "I want a book."
```

## Appendix B — Decision register (project)

| ID | Decision | Status |
|----|----------|--------|
| D1 | IFRA/NLA SNO primary orthography | Resolved |
| D2 | SNO headwords; others = variants | Resolved |
| D3 | Manual-first corpus ethics; no social scraping default | Resolved |
| D4 | Tiered public release; no IFRA guide body without permission | Resolved |
