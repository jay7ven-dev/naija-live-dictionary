/** Sentence normalizer (Part II). Backends: rules | model. */

const DATA = "../data";
const $in = /** @type {HTMLTextAreaElement} */ (document.getElementById("in"));
const $run = /** @type {HTMLButtonElement} */ (document.getElementById("run"));
const $backend = /** @type {HTMLSelectElement} */ (document.getElementById("backend"));
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
/** @type {{ lookup: Record<string, string>, memory: {src:string,tgt:string}[], edits?: {frm:string,to:string}[], max_distance?: number } | null} */
let model = null;

const BOOTSTRAP_EDITS = [
  { frm: "ck", to: "k" },
  { frm: "oo", to: "u" },
  { frm: "ee", to: "i" },
  { frm: "ea", to: "i" },
  { frm: "ph", to: "f" },
  { frm: "wh", to: "w" },
  { frm: "ough", to: "of" },
  { frm: "ight", to: "ite" },
  { frm: "tion", to: "shon" },
  { frm: "c", to: "k" },
];

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

function resolveRules(core) {
  if (!core) return { input: core, output: core, method: "identity", entry_id: null };
  const eid = variantLookup.get(norm(core));
  if (eid) {
    const std = byId.get(eid) ?? core;
    const method = norm(std) === norm(core) ? "identity" : "exact";
    return { input: core, output: std, method, entry_id: eid };
  }
  const nq = norm(core);
  if (nq.length < 2) return { input: core, output: core, method: "unknown", entry_id: null };
  const hits = [];
  for (const { term, id } of fuzzyTerms) {
    const nt = norm(term);
    if (Math.abs(nt.length - nq.length) > fuzzyMaxDistance) continue;
    const d = levenshtein(nq, nt);
    if (d > 0 && d <= fuzzyMaxDistance) hits.push({ d, term, id });
  }
  if (!hits.length) return { input: core, output: core, method: "unknown", entry_id: null };
  hits.sort((a, b) => a.d - b.d || a.term.localeCompare(b.term));
  const tid = hits[0].id;
  return { input: core, output: byId.get(tid) ?? core, method: "fuzzy", entry_id: tid };
}

function resolveModel(core) {
  if (!core || !model) return { input: core, output: core, method: "unknown", entry_id: null };
  const nk = norm(core);
  if (Object.prototype.hasOwnProperty.call(model.lookup, nk)) {
    const tgt = model.lookup[nk];
    const method = norm(tgt) === nk ? "identity" : "model_exact";
    return { input: core, output: tgt, method, entry_id: null };
  }
  // Already a known SNO target — do not NN-corrupt.
  const known = new Set(Object.values(model.lookup || {}).map(norm));
  for (const row of model.memory || []) known.add(norm(row.tgt));
  if (known.has(nk)) {
    return { input: core, output: core, method: "identity", entry_id: null };
  }

  const edits = [...(model.edits || []), ...BOOTSTRAP_EDITS];
  for (const e of edits) {
    if (!e.frm || !nk.includes(e.frm)) continue;
    let cand = nk.replace(e.frm, e.to);
    if (cand !== nk && known.has(cand)) {
      return { input: core, output: cand, method: "model_edit", entry_id: null };
    }
    cand = nk.replace(e.frm, e.to);
    // first-only already covered by replace once; try single replace:
    const idx = nk.indexOf(e.frm);
    if (idx >= 0) {
      cand = nk.slice(0, idx) + e.to + nk.slice(idx + e.frm.length);
      if (cand !== nk && known.has(cand)) {
        return { input: core, output: cand, method: "model_edit", entry_id: null };
      }
    }
  }

  // Weighted vote among neighbors within max_distance.
  const maxD = model.max_distance ?? 2;
  if (nk.length < 2) return { input: core, output: core, method: "unknown", entry_id: null };
  /** @type {Record<string, number>} */
  const scores = {};
  /** @type {Record<string, number>} */
  const bestD = {};
  for (const row of model.memory || []) {
    if (Math.abs(row.src.length - nk.length) > maxD) continue;
    const d = levenshtein(nk, row.src);
    if (d > 0 && d <= maxD) {
      scores[row.tgt] = (scores[row.tgt] || 0) + 1 / d;
      if (bestD[row.tgt] === undefined || d < bestD[row.tgt]) bestD[row.tgt] = d;
    }
  }
  const tgts = Object.keys(scores);
  if (!tgts.length) return { input: core, output: core, method: "unknown", entry_id: null };
  tgts.sort(
    (a, b) =>
      scores[b] - scores[a] || bestD[a] - bestD[b] || b.length - a.length || a.localeCompare(b)
  );
  return { input: core, output: tgts[0], method: "model_nn", entry_id: null };
}

function splitEdge(raw) {
  const m = WORD_RE.exec(raw);
  if (!m) return ["", raw, ""];
  return [raw.slice(0, m.index), m[0], raw.slice(m.index + m[0].length)];
}

function normalizeSentence(text, backend) {
  const parts = text.split(/(\s+)/);
  const tokens = [];
  const outParts = [];
  const resolve = backend === "model" ? resolveModel : resolveRules;
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
    const dec = resolve(core);
    tokens.push(dec);
    outParts.push(`${lead}${dec.output}${trail}`);
  }
  return { input: text, output: outParts.join(""), tokens, backend };
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
  const result = normalizeSentence(text, "rules");
  const fuzzyN = result.tokens.filter((t) =>
    ["fuzzy", "model_nn", "model_edit"].includes(t.method)
  ).length;
  const unkN = result.tokens.filter((t) => t.method === "unknown").length;
  $status.textContent = `Spelling fix (rules) · ${fuzzyN} changed via fuzzy/edit · ${unkN} unknown`;
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
    const res = await fetch("/api/translate", {
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
    $status.textContent = data.pcm_raw && data.pcm_raw !== data.output
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
    const [dictRes, indexRes, fuzzyRes, modelRes] = await Promise.all([
      fetch(`${DATA}/dictionary.json`),
      fetch(`${DATA}/variant_index.json`),
      fetch(`${DATA}/fuzzy_lookup.json`),
      fetch(`${DATA}/normalizer_model.json`),
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
    if (modelRes.ok) {
      model = await modelRes.json();
      $status.textContent = "Ready · English → Pidgin (primary). Spelling fix under the details panel.";
    } else {
      model = null;
      $status.textContent = "Ready · English → Pidgin (primary). Spelling fix uses rules only.";
    }
    window.ComposeAssist.mountComposeAssist({
      input: $in,
      keysEl: document.getElementById("compose-keys"),
      suggestEl: document.getElementById("compose-suggest"),
      catalog: window.ComposeAssist.catalogFromIndex(index, byId),
      enableSuggest: true,
    });
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
    translate();
  }
});

boot();
