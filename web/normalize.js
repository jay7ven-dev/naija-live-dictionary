/** Sentence normalizer (Part II) — Fix spelling via dictionary rules (exact + fuzzy). */

const DATA = "../data";

/** Project root path for APIs ('' locally; '/repo' on GitHub Pages). Static hosts have no translate API. */
function apiRoot() {
  const path = window.location.pathname;
  const i = path.indexOf("/web/");
  return i >= 0 ? path.slice(0, i) : "";
}

const $in = /** @type {HTMLTextAreaElement} */ (document.getElementById("in"));
const $run = /** @type {HTMLButtonElement} */ (document.getElementById("run"));
const $status = document.getElementById("status");
const $out = document.getElementById("out");
const $tokenList = document.getElementById("token-list");
const $translate = /** @type {HTMLButtonElement} */ (document.getElementById("translate"));

/** @type {Map<string, string>} */
let variantLookup = new Map();
/** @type {Map<string, string>} */
let byId = new Map();
/** @type {{ term: string, id: string }[]} */
let fuzzyTerms = [];
let fuzzyMaxDistance = 2;

const WORD_RE =
  /[a-zA-ZàáèéìíòóùúÀÁÈÉÌÍÒÓÙÚ]+(?:[-'][a-zA-ZàáèéìíòóùúÀÁÈÉÌÍÒÓÙÚ]+)*/;

function norm(s) {
  return s.normalize("NFC").toLocaleLowerCase();
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

/**
 * Rules resolve — keep in sync with data/normalize.py resolve_token_rules
 * (short-token fuzzy guards: len<=2 skip; len<=3 → distance 1 + same length).
 */
function resolveRules(core) {
  if (!core) return { input: core, output: core, method: "identity", entry_id: null };
  const eid = variantLookup.get(norm(core));
  if (eid) {
    const std = byId.get(eid) ?? core;
    const method = norm(std) === norm(core) ? "identity" : "exact";
    return { input: core, output: std, method, entry_id: eid };
  }
  const nq = norm(core);
  // Fuzzy on 1–2 letter tokens is almost always English residue noise (be→bed).
  if (nq.length <= 2) return { input: core, output: core, method: "unknown", entry_id: null };

  // 3-letter: same-length edits only, max distance 1 (bok→buk; not be-length traps).
  const lim = nq.length <= 3 ? 1 : fuzzyMaxDistance;

  const hits = [];
  for (const { term, id } of fuzzyTerms) {
    const nt = norm(term);
    if (Math.abs(nt.length - nq.length) > lim) continue;
    if (nq.length <= 3 && nt.length !== nq.length) continue;
    const d = levenshtein(nq, nt);
    if (d > 0 && d <= lim) hits.push({ d, term, id });
  }
  if (!hits.length) return { input: core, output: core, method: "unknown", entry_id: null };
  hits.sort((a, b) => a.d - b.d || a.term.localeCompare(b.term));
  const tid = hits[0].id;
  return { input: core, output: byId.get(tid) ?? core, method: "fuzzy", entry_id: tid };
}

function splitEdge(raw) {
  const m = WORD_RE.exec(raw);
  if (!m) return ["", raw, ""];
  return [raw.slice(0, m.index), m[0], raw.slice(m.index + m[0].length)];
}

function normalizeSentence(text) {
  const parts = text.split(/(\s+)/);
  const tokens = [];
  const outParts = [];
  for (const part of parts) {
    if (part === "" || /^\s+$/.test(part)) {
      outParts.push(part);
      continue;
    }
    const [lead, core, trail] = splitEdge(part);
    const m = core && core.match(WORD_RE);
    if (!core || !m || m[0] !== core) {
      outParts.push(part);
      tokens.push({ input: part, output: part, method: "identity", entry_id: null });
      continue;
    }
    const dec = resolveRules(core);
    tokens.push(dec);
    outParts.push(`${lead}${dec.output}${trail}`);
  }
  return { input: text, output: outParts.join(""), tokens, backend: "rules" };
}

function render(result) {
  $out.textContent = result.output || "—";
  $tokenList.hidden = false;
  $tokenList.innerHTML = "";
  for (const t of result.tokens) {
    if (t.method === "identity" && t.input === t.output && !/[a-zA-Zàáèéìíòóùú]/i.test(t.input)) {
      continue;
    }
    const li = document.createElement("li");
    li.className = `norm-${t.method}`;
    const changed = t.input !== t.output;
    li.textContent = changed
      ? `${t.input} → ${t.output} (${t.method})`
      : `${t.input} (${t.method})`;
    $tokenList.appendChild(li);
  }
}

function run() {
  const text = $in.value;
  if (!text.trim()) {
    $status.textContent = "Paste Pidgin text first (spelling fix only).";
    $out.textContent = "";
    $tokenList.hidden = true;
    return;
  }
  const result = normalizeSentence(text);
  const fuzzyN = result.tokens.filter((t) => t.method === "fuzzy").length;
  const unkN = result.tokens.filter((t) => t.method === "unknown").length;
  $status.textContent = `Spelling fix (rules) · ${fuzzyN} changed via fuzzy · ${unkN} unknown`;
  render(result);
}

async function translate() {
  const text = $in.value.trim();
  if (!text) {
    $status.textContent = "Paste English text first.";
    return;
  }
  $status.textContent = "Translating (first run may download the model)…";
  $status.setAttribute("aria-busy", "true");
  $translate.disabled = true;
  try {
    const res = await fetch(`${apiRoot()}/api/translate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const rawBody = await res.text();
    let data;
    try {
      data = JSON.parse(rawBody);
    } catch {
      throw new Error(
        `Server returned non-JSON (HTTP ${res.status}). ` +
          "Stop all python web/serve.py processes, then start one fresh and hard-refresh this page (Ctrl+F5)."
      );
    }
    if (!res.ok) {
      throw new Error(data.error || res.statusText);
    }
    $status.textContent =
      data.pcm_raw && data.pcm_raw !== data.output
        ? `English → Pidgin · raw MT: ${data.pcm_raw}`
        : "English → Pidgin · SNO spelling applied";
    render({
      output: data.output,
      tokens: data.tokens || [],
      backend: "translate",
    });
  } catch (err) {
    $status.textContent = String(err.message || err);
  } finally {
    $translate.disabled = false;
    $status.removeAttribute("aria-busy");
  }
}

async function boot() {
  $status.textContent = "Loading indexes…";
  $status.setAttribute("aria-busy", "true");
  try {
    const [dictRes, indexRes, fuzzyRes] = await Promise.all([
      fetch(`${DATA}/dictionary.json`),
      fetch(`${DATA}/variant_index.json`),
      fetch(`${DATA}/fuzzy_lookup.json`),
    ]);
    if (!dictRes.ok || !indexRes.ok || !fuzzyRes.ok) {
      throw new Error("Failed to load data files (serve via python web/serve.py)");
    }
    const entries = await dictRes.json();
    const index = await indexRes.json();
    const fuzzy = await fuzzyRes.json();
    byId = new Map(entries.map((e) => [e.id, e.standard_spelling]));
    variantLookup = new Map();
    for (const [k, v] of Object.entries(index)) {
      const nk = norm(k);
      if (!variantLookup.has(nk)) variantLookup.set(nk, v);
    }
    fuzzyTerms = fuzzy.terms ?? [];
    fuzzyMaxDistance = fuzzy.max_distance ?? 2;
    $status.textContent = "Ready · Fix spelling (rules). English → Pidgin under Advanced.";
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
  } catch (err) {
    $status.textContent = String(err.message || err);
  } finally {
    $status.removeAttribute("aria-busy");
  }
}

$run.addEventListener("click", run);
$translate.addEventListener("click", translate);
$in.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
    e.preventDefault();
    run();
  }
});

boot();
