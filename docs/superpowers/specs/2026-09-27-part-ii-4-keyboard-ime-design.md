# Part II-4 — Keyboard / IME (design)

**Status:** Implemented 2026-09-27 — see `docs/phase-ii-4-keyboard-ime.md`. **UI approved via go.**  
**Prior:** II-1 rules normalizer · II-2 thin model · II-3 translate + harden  
**Orthography authority:** IFRA/NLA SNO (D1); Phase 0 digraph/tone inventory  
**UI catalog (for a future impl only):** `docs/design-ui-resources.md` — brainstorming + existing `rankHits` / GOV.UK-style autocomplete notes; no Typesense/Meilisearch

## Locked decisions

| Choice | Value |
|--------|--------|
| This increment | Design then **web compose assist** (approved) |
| First build after approval | **II-4 web compose assist** on existing pages |
| Later | **II-5+ OS / mobile IME** (Windows TSF, Android/iOS) — out of II-4 build |
| Physical layout | English QWERTY base; no custom hardware layout for v1 |
| Lexicon | Never auto-write `dictionary.json` / mappings from the assist |
| Sentence UX | Does **not** replace Option B (EN→Pidgin primary; Fix spelling secondary) |

## Goal

1. Specify how users compose SNO digraphs and tone-marked vowels without leaving the Live Dictionary tooling.  
2. Specify live token suggestions from the existing variant index.  
3. Gate OS-level IME packaging behind a later phase once the web assist proves the digraph + suggest contract.

## Authority inventory (compose targets)

From Phase 0 / IFRA extract (`sources/extractions/ifra-sno-web.txt`):

| Topic | Rule |
|-------|------|
| Digraphs | `ch`, `gb`, `sh`, `kp`, `zh` |
| Letter set | 28 SNO letters (Latin + digraphs) |
| Tone | High acute only (`´`); low unmarked — helpers for `á é í ó ú` on tone words |
| Pragmatism | English-keyboard friendly (Naija Guru alignment on typing ease; IFRA remains headword authority) |

---

## Phase II-4 — Web compose assist (first build after **go**)

### In

1. **Primary surface:** `web/normalize.html` textarea (same chrome as Option B).  
2. **Secondary surface (optional in same increment if cheap):** dictionary search field on `web/`.  
3. **Digraph cheat panel:** clickable inserts for `gb`, `kp`, `sh`, `ch`, `zh` plus acute-vowel helpers; insert at caret (or append).  
4. **Live suggestions:** client-side prefix match against `data/variant_index.json` (and/or fuzzy terms already shipped); reuse existing search ranking patterns in `web/` JS — **no** new search engine.  
5. **Behavior:** suggestion accept replaces the current token; digraph insert never runs Marian or rules normalize automatically.  
6. **Docs:** short phase note `docs/phase-ii-4-keyboard-ime.md` + `PROJECT.md` row → Done when implemented.  
7. **Catalog pick (impl time):** brainstorming + `docs/design-ui-resources.md`; prefer existing `rankHits` / GOV.UK autocomplete notes over Fuse/Typesense.

```text
User types → digraph panel and/or prefix suggest → insert/replace token
         ↛ auto lexicon write
         ↛ replace EN→Pidgin / Fix spelling actions
```

### Out

- Installable OS or mobile IME  
- Neural autocorrect-as-you-type  
- Cloud APIs  
- Custom physical keyboard layout files as the v1 deliverable  
- Claiming assist output as IFRA authority without human/lexicon grounding  

### Check (after implementation — not this increment)

```bash
python web/serve.py
# Browser: /web/normalize.html — digraph insert + suggestion accept
python web/verify.py
```

---

## Phase II-5+ — OS / mobile IME (later)

### In (future)

1. Export the same digraph set + suggest lexicon (derived from `variant_index.json`) for an external IME package.  
2. Windows TSF and/or mobile IMEs as separate packaging tracks.  
3. Consume Live Dictionary updates via regenerated export — still no silent lexicon writes from the IME.

### Out of II-4

Any OS installer, store listing, or system-wide key hook.

---

## UI note

Preserve Live Dictionary chrome (`docs/design-ui-resources.md`). Ponytail: smallest diff on `normalize.html` / shared JS. No new design system. Brainstorming gate for UI is satisfied by this spec once the user replies **go**.

---

## Implementation order (after approval)

1. Spec review (this file) — **current step**.  
2. Digraph panel on `normalize.html`.  
3. Prefix suggest from `variant_index.json`.  
4. Optional dictionary search field parity.  
5. Phase note + roadmap Done.  
6. (Later) II-5 OS IME packaging.

## Spec review gate

**Approved** (user **go**, 2026-09-27). Implementation: `docs/phase-ii-4-keyboard-ime.md`.
