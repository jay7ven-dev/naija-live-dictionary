/**
 * II-4 web compose assist: digraph / acute inserts + prefix suggestions.
 * Shared by normalize.html and (digraph panel) index.html.
 */
(function (global) {
  const DIGRAPHS = ["gb", "kp", "sh", "ch", "zh"];
  const ACUTE = ["á", "é", "í", "ó", "ú"];
  const SUGGEST_MIN = 2;
  const SUGGEST_CAP = 6;
  const WORD_RE =
    /[a-zA-ZàáèéìíòóùúÀÁÈÉÌÍÒÓÙÚ]+(?:[-'][a-zA-ZàáèéìíòóùúÀÁÈÉÌÍÒÓÙÚ]+)*/;

  function norm(s) {
    return s.normalize("NFC").toLocaleLowerCase();
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  /** @param {HTMLInputElement | HTMLTextAreaElement} el @param {string} text */
  function insertAtCaret(el, text) {
    const start = el.selectionStart ?? el.value.length;
    const end = el.selectionEnd ?? start;
    const v = el.value;
    el.value = v.slice(0, start) + text + v.slice(end);
    const pos = start + text.length;
    el.setSelectionRange(pos, pos);
    el.focus();
    el.dispatchEvent(new Event("input", { bubbles: true }));
  }

  /** Current word under caret (or empty). */
  function tokenAtCaret(el) {
    const pos = el.selectionStart ?? 0;
    const v = el.value;
    let i = pos;
    while (i > 0 && /[a-zA-ZàáèéìíòóùúÀÁÈÉÌÍÒÓÙÚ'-]/.test(v[i - 1])) i--;
    let j = pos;
    while (j < v.length && /[a-zA-ZàáèéìíòóùúÀÁÈÉÌÍÒÓÙÚ'-]/.test(v[j])) j++;
    return { start: i, end: j, text: v.slice(i, j) };
  }

  /** @param {string} query @param {{ term: string, id: string, std: string }[]} catalog */
  function prefixSuggest(query, catalog, limit = SUGGEST_CAP) {
    const nq = norm(query);
    if (nq.length < SUGGEST_MIN) return [];
    const ranked = [];
    for (const row of catalog) {
      const nt = norm(row.term);
      if (!nt.startsWith(nq)) continue;
      const isStd = norm(row.std) === nt;
      ranked.push({
        id: row.id,
        term: row.term,
        insert: row.std,
        label: isStd ? row.std : `${row.term} → ${row.std}`,
        tier: isStd ? 0 : 1,
      });
    }
    ranked.sort(
      (a, b) =>
        a.tier - b.tier || a.label.localeCompare(b.label, undefined, { sensitivity: "base" })
    );
    const seen = new Set();
    const out = [];
    for (const r of ranked) {
      const key = `${r.id}:${norm(r.insert)}`;
      if (seen.has(key)) continue;
      seen.add(key);
      out.push(r);
      if (out.length >= limit) break;
    }
    return out;
  }

  /**
   * Build catalog from variant index + id→standard map.
   * @param {Record<string, string>} index
   * @param {Map<string, string>} byIdStd
   */
  function catalogFromIndex(index, byIdStd) {
    /** @type {{ term: string, id: string, std: string }[]} */
    const rows = [];
    for (const [term, id] of Object.entries(index)) {
      const std = byIdStd.get(id) || term;
      rows.push({ term, id, std });
    }
    return rows;
  }

  /**
   * @param {{
   *   input: HTMLInputElement | HTMLTextAreaElement,
   *   keysEl: HTMLElement,
   *   suggestEl?: HTMLElement | null,
   *   catalog?: { term: string, id: string, std: string }[],
   *   enableSuggest?: boolean,
   * }} opts
   */
  function mountComposeAssist(opts) {
    const { input, keysEl } = opts;
    const suggestEl = opts.suggestEl || null;
    const catalog = opts.catalog || [];
    const enableSuggest = Boolean(opts.enableSuggest && suggestEl);
    let items = [];
    let active = -1;

    keysEl.innerHTML = "";
    const mkBtn = (label, insert) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "compose-key";
      b.textContent = label;
      b.setAttribute("aria-label", `Insert ${label}`);
      b.addEventListener("click", () => {
        insertAtCaret(input, insert);
        if (enableSuggest) refreshSuggest();
      });
      keysEl.appendChild(b);
    };
    for (const d of DIGRAPHS) mkBtn(d, d);
    for (const a of ACUTE) mkBtn(a, a);

    if (!enableSuggest) {
      return { insertAtCaret: (t) => insertAtCaret(input, t) };
    }

    function hideSuggest() {
      items = [];
      active = -1;
      suggestEl.innerHTML = "";
      suggestEl.classList.add("hidden");
      input.setAttribute("aria-expanded", "false");
      input.removeAttribute("aria-activedescendant");
    }

    function setActive(i) {
      active = i;
      const optsEls = [...suggestEl.querySelectorAll("[role=option]")];
      optsEls.forEach((el, idx) => {
        el.setAttribute("aria-selected", idx === i ? "true" : "false");
        if (idx === i) input.setAttribute("aria-activedescendant", el.id);
      });
      if (i < 0) input.removeAttribute("aria-activedescendant");
    }

    function applyItem(it) {
      const tok = tokenAtCaret(input);
      const v = input.value;
      input.value = v.slice(0, tok.start) + it.insert + v.slice(tok.end);
      const pos = tok.start + it.insert.length;
      input.setSelectionRange(pos, pos);
      input.focus();
      hideSuggest();
      input.dispatchEvent(new Event("input", { bubbles: true }));
    }

    function refreshSuggest() {
      const tok = tokenAtCaret(input);
      if (!tok.text || !WORD_RE.test(tok.text)) {
        hideSuggest();
        return;
      }
      items = prefixSuggest(tok.text, catalog);
      active = -1;
      if (!items.length) {
        hideSuggest();
        return;
      }
      suggestEl.classList.remove("hidden");
      input.setAttribute("aria-expanded", "true");
      suggestEl.innerHTML = items
        .map(
          (it, i) =>
            `<li role="option" id="compose-opt-${i}" data-i="${i}" aria-selected="false">${escapeHtml(it.label)}</li>`
        )
        .join("");
    }

    suggestEl.addEventListener("mousedown", (e) => {
      const li = e.target instanceof Element ? e.target.closest("[data-i]") : null;
      if (!li) return;
      e.preventDefault();
      const i = Number(li.getAttribute("data-i"));
      if (items[i]) applyItem(items[i]);
    });

    input.addEventListener("input", refreshSuggest);
    input.addEventListener("click", refreshSuggest);
    input.addEventListener("keyup", (e) => {
      if (["ArrowLeft", "ArrowRight", "Home", "End"].includes(e.key)) refreshSuggest();
    });
    input.addEventListener("keydown", (e) => {
      if (!items.length || suggestEl.classList.contains("hidden")) return;
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setActive(Math.min(active + 1, items.length - 1));
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        setActive(Math.max(active - 1, 0));
      } else if (e.key === "Enter" && !e.ctrlKey && !e.metaKey && active >= 0) {
        e.preventDefault();
        applyItem(items[active]);
      } else if (e.key === "Escape") {
        hideSuggest();
      }
    });
    input.addEventListener("blur", () => {
      setTimeout(hideSuggest, 150);
    });

    return { refreshSuggest, hideSuggest, insertAtCaret: (t) => insertAtCaret(input, t) };
  }

  global.ComposeAssist = {
    DIGRAPHS,
    ACUTE,
    insertAtCaret,
    tokenAtCaret,
    prefixSuggest,
    catalogFromIndex,
    mountComposeAssist,
  };
})(typeof window !== "undefined" ? window : globalThis);
