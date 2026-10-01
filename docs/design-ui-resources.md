# Design / UI resources

**Consult this file before any `web/` or UI work.** Do not skip it for search, ranking, variant→standard lookup, visual polish, or a redesign of the Live Dictionary.

**Do not install, clone, or copy uninstalled items** unless the user explicitly approves. Uninstalled rows stay uninstalled; they are listed so they can be chosen later.

**Project direction (selection filter):** Part I Live Dictionary — static HTML/CSS/JS in `web/`, IFRA/NLA SNO spelling authority, teaching + lookup tool, Ponytail/YAGNI. Part II: **Fix spelling (rules) primary** on `normalize.html`; English→Pidgin Advanced; Keyman II-5b Done; web compose (II-4) removed; native store IMEs deferred (II-5c+).

Source conversation for the search/UX slice: `conversation-export_1.md` (Dictionary Project — Status Table & UI Improvement). **IFRA** here means IFRA/NLA Standard Naijá Orthography, not infrastructure.

---

## Agent procedure (planning-doc rule)

This is the UI instance of the project rule: **use `brainstorming` before schema, D1, UI, or pipeline design** (`PROJECT.md`; `.cursor/rules/pidgin-project.mdc`; `.agents/skills/brainstorming/SKILL.md`).

For web/UI tasks, run that gate **from this file**:

1. Read `PROJECT.md` (Part I scope, YAGNI, `web/` already ships browse + search + variant→standard).
2. Attach **`brainstorming`**. Do not implement until a design is approved.
3. Read this catalog. Match **task type** to a row (visual polish vs search ranking vs autocomplete vs extracting a new source).
4. **Select one primary skill or resource** that fits the task *and* the project direction. Prefer project-local skills, then already-installed machine skills, then uninstalled items only if the user approves install.
5. Name the choice and why the others lose (stack, scale, marketing-vs-tool, Part II).
6. After approval, implement with Ponytail (smallest diff in `web/`). Verify with `python web/verify.py`.

**No design-taste skill is attached to this project.** `.agents/skills/` has method skills only (`brainstorming`, `tapestry`, `skill-seekers`, `learn-this`, `article-extractor`, `ship-learn-next`). Taste/UI skills live on the machine (`.claude/skills/`) or are uninstalled. Do not treat that gap as permission to skip this file or to install a taste skill unprompted.

---

## How to pick (this product)

| Task | First pick | Usually not |
|------|------------|-------------|
| Any UI change | `brainstorming` + this file | Jumping to implementation |
| Critique / polish existing `web/` | **impeccable** (`critique` then `polish` / `quieter` / `layout` / `interaction-design`); **redesign-skill** if the pass is a visual upgrade in place | `gpt-tasteskill`, imagegen, brandkit |
| Public-tool a11y, spacing, search-field behaviour | GOV.UK autocomplete notes; **web-design-guidelines** (uninstalled) | Typesense / Meilisearch at current scale |
| Fuzzy / typo / ranking | Keep existing `rankHits` / `matchTier`; **uFuzzy** only if custom ranking is not enough | Fuse.js unless uFuzzy is rejected; full search engines |
| New visual source of truth (`DESIGN.md`) | **stitch-skill** or a file from awesome-design-md — only if the user wants one | Copying the Nike gym `DESIGN.md` as this product’s look |
| Orthography / source pages (not chrome) | `tapestry` / `learn-this` / `article-extractor` / `ship-learn-next` | Frontend taste skills |
| Package a persistent orthography skill | `skill-seekers` | Design-taste skills |
| Analysis tables / investigations in Cursor | Cursor **canvas** skill | Using canvas as the dictionary UI |

Live Dictionary today: debounce (~120ms), variant banner, layered ranking. **uFuzzy, Fuse.js, Meilisearch, and Typesense are not in the repo.**

---

## A. Project-local skills (`.agents/skills/`) — installed here

None of these is a design-taste skill. They still belong in UI planning because the planning-doc rule routes creative work through them, and source-extraction skills feed content the UI displays.

| Skill | Path | Source | When |
|-------|------|--------|------|
| **brainstorming** | `.agents/skills/brainstorming/` | https://github.com/obra/superpowers/tree/main/skills/brainstorming | **Required** before schema, D1, UI, or pipeline design. For UI: brainstorm *using this file*, then pick a specialist. Specs: `docs/superpowers/specs/` |
| **skill-seekers** | `.agents/skills/skill-seekers/` | https://github.com/yusufkaraaslan/Skill_Seekers | Package IFRA/Naija Guru into a persistent orthography skill — not visual UI |
| **tapestry** | `.agents/skills/tapestry/` | project bundle | Phase 0 weave of orthography sources |
| **learn-this** | `.agents/skills/learn-this/` | Tapestry | Extract URL/PDF → plan |
| **article-extractor** | `.agents/skills/article-extractor/` | Tapestry | Clean extract of IFRA / Naija Guru / UX articles |
| **ship-learn-next** | `.agents/skills/ship-learn-next/` | Tapestry | Turn extracts into shippable steps |

Standing (not under `.agents/skills/`): `/kybernetes-loop-governor`, `/ponytail`, `/user-prompting-style`.

---

## B. Design / UI skills — installed on this machine, **not** in the Pidgin repo

Location: `~/.claude/skills/` (machine-local Claude skills). Cursor’s project skill list does not include them; attach explicitly when chosen.

### High fit for `web/` (existing tool UI)

| Skill | Path | Upstream | Use |
|-------|------|----------|-----|
| **impeccable** | `.claude\skills\impeccable` | https://github.com/pbakaus/impeccable · https://www.skills.sh/pbakaus/impeccable | critique / audit / polish / quieter / layout / interaction-design on product UI. Subcommands: `reference/*.md` (`critique`, `polish`, `quieter`, `bolder`, `distill`, `delight`, `layout`, `interaction-design`, `audit`, …). Product register (`reference/product.md`), not brand/landing. |
| **redesign-skill** | `.claude\skills\redesign-skill` | (no `source:` in frontmatter) | Scan → diagnose → upgrade in place; no rewrite |
| **emil-design-eng** | `.claude\skills\emil-design-eng` | https://github.com/emilkowalski/skill | Search-field polish, motion, craft |
| **review-animations** | `.claude\skills\review-animations` | pairs with Emil / https://animations.dev/ | Review motion only |
| **minimalist-skill** | `.claude\skills\minimalist-skill` | local | Editorial / dictionary-like chrome |
| **stitch-skill** | `.claude\skills\stitch-skill` | Google Stitch; https://labs.google/stitch | Generate `DESIGN.md` for Stitch screens — only if using Stitch |

### Installed, weaker fit (landing / marketing / motion-heavy)

| Skill | Path | Note |
|-------|------|------|
| taste-skill / taste-skill-v1 | `.claude\skills\taste-skill*` | https://github.com/Leonxlnx/taste-skill — skill says **not** dashboards/data tables |
| gpt-tasteskill | `.claude\skills\gpt-tasteskill` | GSAP / Awwwards; fights static `web/` |
| brutalist-skill | `.claude\skills\brutalist-skill` | Possible look; high visual risk for a teaching dictionary |
| imagegen-frontend-web / mobile | `.claude\skills\imagegen-frontend-*` | Mockup images, not the live app |
| image-to-code-skill | `.claude\skills\image-to-code-skill` | Image-first marketing sites |
| brandkit | `.claude\skills\brandkit` | Identity boards, not search UX |
| animation-vocabulary | `.claude\skills\animation-vocabulary` | Naming motion, not implementing it |

**Cursor built-in:** `canvas` at `.cursor\skills-cursor\canvas` — analysis canvases beside chat, not the dictionary UI.

---

## C. Design skills / repos — **uninstalled**

Do not run these until approved. Catalog: https://www.skills.sh/topic/design · browse: https://skills.sh/

| Skill / repo | URL | Install command (do not run yet) | Why it is listed |
|--------------|-----|----------------------------------|------------------|
| **frontend-design** | https://www.skills.sh/anthropics/skills/frontend-design | `npx skills add https://github.com/anthropics/skills --skill frontend-design` | Official anti-slop frontend |
| **web-design-guidelines** | vercel-labs/agent-skills | `npx skills add vercel-labs/agent-skills --skill web-design-guidelines` | Spacing, type, a11y — closest to public-tool chrome |
| vercel-composition-patterns | same repo | (React composition) | Low fit: this UI is not React |
| **ui-ux-pro-max** | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | `npx skills add nextlevelbuilder/ui-ux-pro-max-skill` | Complex interaction patterns |
| canvas-design | anthropics/skills | skills.sh listing | Canvas generation, not this static site |
| extract-design-system | arvindrk/extract-design-system | skills.sh listing | Tokenize existing CSS if a system is grown |
| sleek-design-mobile-apps | sleekdotdesign/agent-skills | skills.sh listing | Mobile apps — Part II / out of Part I |
| **awesome-design-md** | https://github.com/VoltAgent/awesome-design-md | clone / copy a `DESIGN.md` | Brand DESIGN.md files for agents |
| ComposioHQ/awesome-claude-skills | catalog (via find-skills) | — | Index of skills, not a single UI skill |
| find-skills (method) | `~/.agents/skills/find-skills/` | `npx skills find [query]` | Discover more; still requires user approval to add |

**Recommended first uninstalled skill if one is added later:** `web-design-guidelines` (a11y / public-tool), not a marketing taste pack.

---

## D. Search / UX libraries and references

### From the status-table / UI-improvement conversation

| Resource | URL | Status | Fit |
|----------|-----|--------|-----|
| TEI Lex-0 (CLARIN) | https://standards.clarin.eu/sis/views/view-format.xq?id=fLex0 | reference | Schema/docs, not chrome |
| TEI Lex-0 (HAL) | https://hal.science/hal-01757108v1 | reference | Same |
| **uFuzzy** | https://github.com/leeoniya/uFuzzy | **uninstalled** (library) | Strongest client-side fuzzy for short headwords |
| **Typesense** | https://github.com/typesense/typesense | **uninstalled** (engine) | Overkill at ~383 entries / ~826 index keys |
| Meilisearch relevance | https://www.meilisearch.com/blog/search-relevance | reference | Ranking model: typo ≠ synonym |
| GOV.UK search autocomplete | https://design-guide.publishing.service.gov.uk/components/search-autocomplete/ | reference | When to autocomplete; ~3-char threshold; cap ~5 suggestions |
| Figma forum: typo-tolerant search | https://forum.figma.com/t/better-component-finders-adding-typo-tolerant-search-for-enhanced-usability/50981 | reference | Typo tolerance as baseline UX |
| **Fuse.js** | https://github.com/krisk/Fuse | **uninstalled** (library) | Named in the export; second client-side option after uFuzzy |

### Expanded from that list (still uninstalled / reference-only)

| Resource | URL | Why |
|----------|-----|-----|
| GOV.UK Accessible Autocomplete | https://alphagov.github.io/accessible-autocomplete/ | ARIA component; progressive enhancement |
| Meilisearch typo internals | https://www.meilisearch.com/docs/resources/internals/typo_tolerance | Edit distance by word length; hard cap 2 |
| Prefix autocomplete + typo | https://sujeet.pro/articles/design-search-autocomplete | Damerau–Levenshtein; disable typo below ~3 chars; distance 1 for short words |
| Autocomplete system notes | https://systeminternals.dev/system-design-interview/search-autocomplete/ | Debounce ~150ms; exact → 1-edit → 2-edit tiers |

**Reddit (requested in the export; no durable threads captured):** [r/userexperience](https://www.reddit.com/r/userexperience/), [r/UI_Design](https://www.reddit.com/r/UI_Design/), [r/web_design](https://www.reddit.com/r/web_design/).

---

## E. Local clones and Hussell-folder artifacts (not in this repo)

| Location | What |
|----------|------|
| `~/design-skill-src/` (optional local clones) | Prior session clones: `awesome` (VoltAgent/awesome-design-md), `emil` (emilkowalski/skill), `impeccable` (pbakaus/impeccable), `taste` (Leonxlnx/taste-skill) |
| Sibling Hussell folder `Website COde_File/.../DESIGN.md` | Stitch-style Nike DESIGN.md — commerce look; **not** this dictionary’s visual identity |
| Sibling Hussell folder `Project tracker/...` | Tracker-only skills / separate tracker UI — not Pidgin UI |
| This project `docs/phase-4-web-ui.md` | What the Live Dictionary UI already does |

This project has **no** `DESIGN.md` of its own.

---

## F. In-repo UI docs (existing)

| File | Role |
|------|------|
| `docs/phase-4-web-ui.md` | Phase 4 complete: serve, verify, features |
| `docs/canonical/for-developers.md` | Architecture including `web/` |
| `web/index.html`, `web/` CSS/JS | Implementation |

---

## Short list if recording/installing later

1. Keep using **brainstorming** + this file (already attached).
2. **impeccable** (`critique` → `polish` / `quieter`) — installed globally.
3. **redesign-skill** — installed globally.
4. **web-design-guidelines** — uninstalled; first candidate if a taste/a11y skill is attached to the project.
5. **uFuzzy** — uninstalled library; only if custom ranking is insufficient.
6. GOV.UK autocomplete + accessible-autocomplete — pattern + component.

Omit from a first attach: Typesense/Meilisearch, gpt-tasteskill / imagegen / brandkit, Vercel React composition, mobile skills.
