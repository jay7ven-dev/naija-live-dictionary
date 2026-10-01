/** @typedef {{ id: string, standard_spelling: string, informal_variants?: string[], part_of_speech: string, definitions: string[], example_sentences: string[], notes?: string, pronunciation?: string }} Entry */

/** @typedef {{ term: string, id: string }} FuzzyTerm */

const DATA = "../data";
const $q = /** @type {HTMLInputElement} */ (document.getElementById("q"));
const $status = document.getElementById("status");
const $results = document.getElementById("results");
const $redirect = document.getElementById("redirect");
const $suggest = document.getElementById("suggest");

const SUGGEST_MIN = 3;
const SUGGEST_CAP = 5;
let suggestItems = [];
let suggestActive = -1;

/** @type {Entry[]} */
let entries = [];
/** @type {Map<string, string>} norm -> entry id */
let variantLookup = new Map();
/** @type {Map<string, Entry>} */
let byId = new Map();
/** @type {FuzzyTerm[]} */
let fuzzyTerms = [];
let fuzzyMaxDistance = 2;

function norm(s) {
  return s.trim().normalize("NFC").toLocaleLowerCase();
}

/** @param {string} a @param {string} b */
function levenshtein(a, b) {
  if (a === b) return 0;
  if (!a.length) return b.length;
  if (!b.length) return a.length;
  const row = Array.from({ length: b.length + 1 }, (_, i) => i);
  for (let i = 1; i <= a.length; i++) {
    let prev = i;
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      const next = Math.min(row[j] + 1, prev + 1, row[j - 1] + cost);
      row[j - 1] = prev;
      prev = next;
    }
    row[b.length] = prev;
  }
  return row[b.length];
}

/** @returns {{ term: string, id: string, distance: number }[]} */
function fuzzySuggest(query, limit = 3) {
  const nq = norm(query);
  if (!nq || nq.length < 2) return [];
  const hits = [];
  for (const { term, id } of fuzzyTerms) {
    const nt = norm(term);
    if (Math.abs(nt.length - nq.length) > fuzzyMaxDistance) continue;
    const d = levenshtein(nq, nt);
    if (d > 0 && d <= fuzzyMaxDistance) hits.push({ term, id, distance: d });
  }
  hits.sort((a, b) => a.distance - b.distance || a.term.localeCompare(b.term));
  const seen = new Set();
  const out = [];
  for (const h of hits) {
    if (seen.has(h.id)) continue;
    seen.add(h.id);
    out.push(h);
    if (out.length >= limit) break;
  }
  return out;
}

/**
 * GOV.UK-style query suggestions: prefix only, after 3 chars, cap 5.
 * @returns {{ id: string, term: string, label: string }[]}
 */
function prefixSuggest(query, limit = SUGGEST_CAP) {
  const nq = norm(query);
  if (nq.length < SUGGEST_MIN) return [];
  const ranked = [];
  for (const e of entries) {
    const std = e.standard_spelling;
    if (norm(std).startsWith(nq)) {
      ranked.push({ id: e.id, term: std, label: std, tier: 0 });
    }
    for (const v of e.informal_variants ?? []) {
      if (norm(v).startsWith(nq)) {
        ranked.push({ id: e.id, term: v, label: `${v} → ${std}`, tier: 1 });
      }
    }
  }
  ranked.sort((a, b) => a.tier - b.tier || a.label.localeCompare(b.label, undefined, { sensitivity: "base" }));
  const seen = new Set();
  const out = [];
  for (const r of ranked) {
    const key = `${r.id}:${norm(r.term)}`;
    if (seen.has(key)) continue;
    seen.add(key);
    out.push({ id: r.id, term: r.term, label: r.label });
    if (out.length >= limit) break;
  }
  return out;
}

function hideSuggest() {
  suggestItems = [];
  suggestActive = -1;
  $suggest.innerHTML = "";
  $suggest.classList.add("hidden");
  $q.setAttribute("aria-expanded", "false");
  $q.removeAttribute("aria-activedescendant");
}

function setSuggestActive(i) {
  const opts = [...$suggest.querySelectorAll("[role=option]")];
  suggestActive = i;
  opts.forEach((el, idx) => {
    const on = idx === i;
    el.setAttribute("aria-selected", on ? "true" : "false");
    if (on) $q.setAttribute("aria-activedescendant", el.id);
  });
  if (i < 0) $q.removeAttribute("aria-activedescendant");
}

function renderSuggest(query) {
  const items = prefixSuggest(query);
  suggestItems = items;
  suggestActive = -1;
  if (!items.length) {
    hideSuggest();
    return;
  }
  $suggest.classList.remove("hidden");
  $q.setAttribute("aria-expanded", "true");
  $suggest.innerHTML = items
    .map(
      (it, i) =>
        `<li role="option" id="suggest-${i}" data-term="${escapeHtml(it.term)}" aria-selected="false">${escapeHtml(it.label)}</li>`
    )
    .join("");
}

function applySuggest(term) {
  $q.value = term;
  hideSuggest();
  onSearch();
}

async function load() {
  const [dictRes, indexRes, fuzzyRes] = await Promise.all([
    fetch(`${DATA}/dictionary.json`),
    fetch(`${DATA}/variant_index.json`),
    fetch(`${DATA}/fuzzy_lookup.json`),
  ]);
  if (!dictRes.ok || !indexRes.ok) {
    throw new Error("Failed to load dictionary data. Run the local server from project root.");
  }
  entries = await dictRes.json();
  const index = await indexRes.json();
  byId = new Map(entries.map((e) => [e.id, e]));
  variantLookup = new Map();
  for (const [variant, id] of Object.entries(index)) {
    variantLookup.set(norm(variant), id);
  }
  if (fuzzyRes.ok) {
    const fuzzy = await fuzzyRes.json();
    fuzzyTerms = fuzzy.terms ?? [];
    fuzzyMaxDistance = fuzzy.max_distance ?? 2;
  } else {
    fuzzyTerms = [...variantLookup.entries()].map(([term, id]) => ({ term, id }));
  }
  $results.removeAttribute("aria-busy");
  $status.textContent = `${entries.length} entries loaded`;
  const grownEl = document.getElementById("last-grown");
  if (grownEl) {
    try {
      const gRes = await fetch(`${DATA}/last_grown.json`);
      if (gRes.ok) {
        const g = await gRes.json();
        grownEl.textContent = g.date ? `Lexicon last grown ${g.date}` : "";
      }
    } catch {
      /* optional */
    }
  }
  renderIdle();
}

function entryMatches(entry, nq) {
  if (norm(entry.standard_spelling).includes(nq)) return true;
  if (entry.informal_variants?.some((v) => norm(v).includes(nq))) return true;
  if (entry.definitions.some((d) => norm(d).includes(nq))) return true;
  if (entry.example_sentences.some((ex) => norm(ex).includes(nq))) return true;
  if (norm(entry.id).includes(nq)) return true;
  return false;
}

/**
 * Lower = more relevant. Hierarchy:
 * 0 exact headword · 1 exact variant · 2 headword/id prefix · 3 variant contains
 * 4 definition · 5 example · 6 weak id/other
 * @param {Entry} entry
 * @param {string} nq normalized query
 * @param {Entry | null} exact resolveExact hit
 */
function matchTier(entry, nq, exact) {
  if (exact && entry.id === exact.id) {
    return norm(entry.standard_spelling) === nq ? 0 : 1;
  }
  const std = norm(entry.standard_spelling);
  if (std === nq) return 0;
  const vars = entry.informal_variants ?? [];
  if (vars.some((v) => norm(v) === nq)) return 1;
  const idn = norm(entry.id);
  if (std.startsWith(nq) || idn === nq || idn.startsWith(nq)) return 2;
  if (vars.some((v) => norm(v).includes(nq))) return 3;
  if (entry.definitions.some((d) => norm(d).includes(nq))) return 4;
  if (entry.example_sentences.some((ex) => norm(ex).includes(nq))) return 5;
  if (std.includes(nq) || idn.includes(nq)) return 2;
  return 6;
}

/** @param {Entry[]} hits @param {string} nq @param {Entry | null} exact */
function rankHits(hits, nq, exact) {
  return [...hits].sort((a, b) => {
    const ta = matchTier(a, nq, exact);
    const tb = matchTier(b, nq, exact);
    if (ta !== tb) return ta - tb;
    return a.standard_spelling.localeCompare(b.standard_spelling, undefined, { sensitivity: "base" });
  });
}

/** @returns {Entry | null} */
function resolveExact(query) {
  const nq = norm(query);
  if (!nq) return null;
  const id = variantLookup.get(nq);
  if (id && byId.has(id)) return byId.get(id);
  return entries.find((e) => norm(e.standard_spelling) === nq) ?? null;
}

/** @param {Entry} entry */
function renderCard(entry) {
  const vars =
    entry.informal_variants?.length
      ? `<p class="variants">Variants: ${entry.informal_variants.map((v) => `<code>${escapeHtml(v)}</code>`).join(", ")}</p>`
      : "";
  const pron = entry.pronunciation
    ? `<p class="pron">Pronunciation: <span class="pron-hint">${escapeHtml(entry.pronunciation)}</span></p>`
    : "";
  const notes = entry.notes ? `<p class="notes">${escapeHtml(entry.notes)}</p>` : "";
  return `<article class="card" data-id="${escapeHtml(entry.id)}">
    <div class="card-head">
      <span class="lemma">${escapeHtml(entry.standard_spelling)}</span>
      <span class="pos">${escapeHtml(entry.part_of_speech)}</span>
    </div>
    <ul class="defs">${entry.definitions.map((d) => `<li>${escapeHtml(d)}</li>`).join("")}</ul>
    <ul class="examples">${entry.example_sentences
      .map((ex, i) =>
        i === 0
          ? `<li>${escapeHtml(ex)}</li>`
          : `<li class="example-secondary"><span class="ex-label">Also:</span> ${escapeHtml(ex)}</li>`
      )
      .join("")}</ul>
    ${pron}${vars}${notes}
  </article>`;
}

function escapeHtml(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function renderIdle() {
  hideSuggest();
  $redirect.classList.add("hidden");
  $redirect.innerHTML = "";
  $results.innerHTML = `<p class="idle">Type a spelling to look up the IFRA/NLA standard form. After three letters, suggestions appear under the field.</p>
    <p class="idle-actions"><button type="button" class="text-btn" data-browse>Browse first 40 entries</button></p>`;
  $status.textContent = `${entries.length} entries loaded`;
}

function renderBrowse() {
  hideSuggest();
  const sorted = [...entries].sort((a, b) =>
    a.standard_spelling.localeCompare(b.standard_spelling, undefined, { sensitivity: "base" })
  );
  $results.innerHTML = sorted.slice(0, 40).map(renderCard).join("");
  $redirect.classList.add("hidden");
  $status.textContent = `${entries.length} entries · showing first 40`;
}

function onSearch() {
  const raw = $q.value.trim();
  $redirect.classList.add("hidden");
  $redirect.innerHTML = "";

  if (!raw) {
    renderIdle();
    return;
  }

  const nq = norm(raw);
  const exact = resolveExact(raw);
  if (exact) hideSuggest();
  else renderSuggest(raw);
  const isVariantRedirect = exact && norm(exact.standard_spelling) !== nq;

  let hits = entries.filter((e) => entryMatches(e, nq));
  if (exact && !hits.some((e) => e.id === exact.id)) {
    hits = [exact, ...hits];
  }
  hits = rankHits(hits, nq, exact);

  if (isVariantRedirect && exact) {
    $redirect.classList.remove("hidden");
    $redirect.innerHTML = `Informal spelling <strong>${escapeHtml(raw)}</strong> → standard <strong>${escapeHtml(exact.standard_spelling)}</strong> (IFRA SNO)`;
  }

  if (!hits.length) {
    const fuzzy = fuzzySuggest(raw);
    if (fuzzy.length) {
      const top = fuzzy[0];
      const entry = byId.get(top.id);
      if (entry) {
        $redirect.classList.remove("hidden");
        $redirect.innerHTML = `No exact match for “${escapeHtml(raw)}”. Did you mean <button type="button" class="linkish" data-suggest="${escapeHtml(top.term)}"><strong>${escapeHtml(top.term)}</strong></button> → ${escapeHtml(entry.standard_spelling)}?`;
        $results.innerHTML = fuzzy
          .map(({ term, id }) => {
            const e = byId.get(id);
            return e ? renderCard(e) : "";
          })
          .join("");
        $status.textContent = `${fuzzy.length} fuzzy suggestion${fuzzy.length === 1 ? "" : "s"}`;
        return;
      }
    }
    $results.innerHTML = `<p class="empty">No match for “${escapeHtml(raw)}”. Try another spelling or variant.</p>`;
    $status.textContent = "0 results";
    return;
  }

  $results.innerHTML = hits.slice(0, 50).map(renderCard).join("");
  $status.textContent = `${hits.length} result${hits.length === 1 ? "" : "s"}${hits.length > 50 ? " (first 50)" : ""}`;
}

let debounce = 0;
$q.addEventListener("input", () => {
  clearTimeout(debounce);
  debounce = window.setTimeout(onSearch, 120);
});

$q.addEventListener("keydown", (ev) => {
  if ($suggest.classList.contains("hidden") || !suggestItems.length) return;
  if (ev.key === "ArrowDown") {
    ev.preventDefault();
    setSuggestActive(Math.min(suggestActive + 1, suggestItems.length - 1));
  } else if (ev.key === "ArrowUp") {
    ev.preventDefault();
    setSuggestActive(Math.max(suggestActive - 1, 0));
  } else if (ev.key === "Enter" && suggestActive >= 0) {
    ev.preventDefault();
    applySuggest(suggestItems[suggestActive].term);
  } else if (ev.key === "Escape") {
    hideSuggest();
  }
});

$suggest.addEventListener("mousedown", (ev) => {
  const opt = ev.target instanceof Element ? ev.target.closest("[data-term]") : null;
  if (!opt) return;
  ev.preventDefault();
  applySuggest(opt.getAttribute("data-term") ?? "");
});

$redirect.addEventListener("click", (ev) => {
  const btn = ev.target instanceof Element ? ev.target.closest("[data-suggest]") : null;
  if (!btn) return;
  const term = btn.getAttribute("data-suggest");
  if (!term) return;
  $q.value = term;
  onSearch();
});

$results.addEventListener("click", (ev) => {
  const btn = ev.target instanceof Element ? ev.target.closest("[data-browse]") : null;
  if (!btn) return;
  renderBrowse();
});

$status.textContent = "Loading dictionary…";
$results.setAttribute("aria-busy", "true");

load().catch((err) => {
  $results.removeAttribute("aria-busy");
  $status.textContent = "Dictionary data could not load.";
  $results.innerHTML = `<p class="empty"><strong>Local server required.</strong> Do not open this file directly from disk.<br><br>
    From the project folder run:<br>
    <code>python web/serve.py</code><br><br>
    Then open <a href="http://localhost:8765/web/">http://localhost:8765/web/</a><br>
    <span class="err-detail">${escapeHtml(err.message)}</span></p>`;
});

// ponytail: self-check when run as module in browser with ?test=1
if (new URLSearchParams(location.search).get("test") === "1") {
  load().then(() => {
    const exact = resolveExact("kom");
    const hits = rankHits(
      entries.filter((e) => entryMatches(e, norm("kom"))),
      norm("kom"),
      exact
    );
    const checks = [
      resolveExact("pickin")?.id === "pikin",
      resolveExact("book")?.id === "buk",
      resolveExact("dey")?.id === "de-copula",
      entries.length >= 300,
      exact?.id === "kom",
      hits[0]?.id === "kom",
      prefixSuggest("pic").length >= 1 && prefixSuggest("pic").length <= 5,
      prefixSuggest("pi").length === 0,
    ];
    console.assert(checks.every(Boolean), "smoke checks failed", checks);
  });
}
