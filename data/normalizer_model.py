#!/usr/bin/env python3
"""Train / load a thin orthographic normalizer from curated (variant -> SNO) pairs.

stdlib only. Does not write dictionary.json or variant_mappings.json.
"""
from __future__ import annotations

import json
import random
import re
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICT_PATH = ROOT / "data" / "dictionary.json"
MAPPINGS_PATH = ROOT / "data" / "variant_mappings.json"
MODEL_PATH = ROOT / "data" / "normalizer_model.json"
HELDOUT_PATH = ROOT / "data" / "normalizer_heldout.jsonl"

WORD_RE = re.compile(
    r"^[a-zA-ZàáèéìíòóùúÀÁÈÉÌÍÒÓÙÚ]+(?:[-'][a-zA-ZàáèéìíòóùúÀÁÈÉÌÍÒÓÙÚ]+)*$"
)


def norm_key(s: str) -> str:
    return unicodedata.normalize("NFC", s).casefold()


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cost = 0 if ca == cb else 1
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost))
        prev = cur
    return prev[-1]


def collect_pairs() -> list[dict]:
    """Curated supervision only: informal_variants + variant_mappings -> standard_spelling."""
    entries = json.loads(DICT_PATH.read_text(encoding="utf-8"))
    by_id = {e["id"]: e for e in entries}
    pairs: dict[str, dict] = {}

    def add(src: str, tgt: str, entry_id: str, origin: str) -> None:
        src, tgt = src.strip(), tgt.strip()
        if not src or not tgt:
            return
        if not WORD_RE.match(src) or not WORD_RE.match(tgt):
            return
        if norm_key(src) == norm_key(tgt):
            return
        pairs[norm_key(src)] = {
            "src": src,
            "tgt": tgt,
            "entry_id": entry_id,
            "origin": origin,
        }

    for e in entries:
        std = e["standard_spelling"]
        eid = e["id"]
        for v in e.get("informal_variants") or []:
            add(v, std, eid, "informal_variants")

    if MAPPINGS_PATH.is_file():
        mappings = json.loads(MAPPINGS_PATH.read_text(encoding="utf-8"))
        for m in mappings.get("mappings", []):
            eid = m.get("entry_id")
            e = by_id.get(eid)
            if not e:
                continue
            add(m["variant"], e["standard_spelling"], eid, "variant_mappings")

    return sorted(pairs.values(), key=lambda r: norm_key(r["src"]))


def split_pairs(
    pairs: list[dict], holdout_frac: float = 0.2, seed: int = 42
) -> tuple[list[dict], list[dict]]:
    rng = random.Random(seed)
    shuffled = list(pairs)
    rng.shuffle(shuffled)
    n_hold = max(1, int(round(len(shuffled) * holdout_frac))) if shuffled else 0
    if len(shuffled) >= 2 and n_hold >= len(shuffled):
        n_hold = len(shuffled) - 1
    holdout = shuffled[:n_hold]
    train = shuffled[n_hold:]
    return train, holdout


def _mid_substitution(src: str, tgt: str) -> tuple[str, str] | None:
    """Strip shared prefix/suffix; return (mid_src, mid_tgt) if a small edit."""
    i = 0
    while i < len(src) and i < len(tgt) and src[i] == tgt[i]:
        i += 1
    j = 0
    while (
        j < len(src) - i
        and j < len(tgt) - i
        and src[-(j + 1)] == tgt[-(j + 1)]
    ):
        j += 1
    mid_s = src[i : len(src) - j] if j else src[i:]
    mid_t = tgt[i : len(tgt) - j] if j else tgt[i:]
    if mid_s == mid_t:
        return None
    if len(mid_s) > 5 or len(mid_t) > 5:
        return None
    return mid_s, mid_t


def learn_edits(subset: list[dict], min_count: int = 2) -> list[dict]:
    """Frequent mid-string substitutions attested in train pairs."""
    counts: Counter[tuple[str, str]] = Counter()
    for p in subset:
        mid = _mid_substitution(norm_key(p["src"]), norm_key(p["tgt"]))
        if mid:
            counts[mid] += 1
    edits = [
        {"frm": a, "to": b, "count": c}
        for (a, b), c in counts.most_common()
        if c >= min_count and (a or b)
    ]
    # Prefer longer frm, then higher count (applied in that order at resolve).
    edits.sort(key=lambda e: (-len(e["frm"]), -e["count"], e["frm"], e["to"]))
    return edits


# High-precision English→SNO phonetic shortcuts (Lin subset), used only if result ∈ known SNO.
BOOTSTRAP_EDITS = [
    {"frm": "ck", "to": "k", "count": 0},
    {"frm": "oo", "to": "u", "count": 0},
    {"frm": "ee", "to": "i", "count": 0},
    {"frm": "ea", "to": "i", "count": 0},
    {"frm": "ph", "to": "f", "count": 0},
    {"frm": "wh", "to": "w", "count": 0},
    {"frm": "ough", "to": "of", "count": 0},
    {"frm": "ight", "to": "ite", "count": 0},
    {"frm": "tion", "to": "shon", "count": 0},
    {"frm": "c", "to": "k", "count": 0},
]


def apply_edits(nk: str, edits: list[dict], known_tgt: set[str]) -> str | None:
    """Try learned then bootstrap edits; accept first candidate that lands on known SNO."""
    for e in list(edits) + BOOTSTRAP_EDITS:
        frm, to = e["frm"], e["to"]
        if not frm or frm not in nk:
            continue
        cand = nk.replace(frm, to, 1)
        if cand != nk and cand in known_tgt:
            return cand
        # also try replace-all for short digraphs
        if len(frm) >= 2:
            cand2 = nk.replace(frm, to)
            if cand2 != nk and cand2 in known_tgt:
                return cand2
    return None


def train_model(
    holdout_frac: float = 0.2,
    seed: int = 42,
    model_path: Path = MODEL_PATH,
    heldout_path: Path = HELDOUT_PATH,
) -> dict:
    pairs = collect_pairs()
    train, holdout = split_pairs(pairs, holdout_frac=holdout_frac, seed=seed)

    def pack(subset: list[dict], *, n_holdout: int, holdout_srcs: set[str] | None = None) -> dict:
        lookup = {norm_key(p["src"]): p["tgt"] for p in subset}
        memory = [{"src": norm_key(p["src"]), "tgt": p["tgt"]} for p in subset]
        # Augment with Lin-style informal spellings of train targets (never holdout srcs).
        try:
            from lin_variants import generate_variants
        except ImportError:
            generate_variants = None  # type: ignore
        blocked = holdout_srcs or set()
        if generate_variants:
            for p in subset:
                tgt = p["tgt"]
                for v in generate_variants(tgt, max_variants=12):
                    nk = norm_key(v)
                    if nk in blocked or nk in lookup or nk == norm_key(tgt):
                        continue
                    lookup[nk] = tgt
                    memory.append({"src": nk, "tgt": tgt})
        return {
            "version": 2,
            "backend": "model",
            "type": "exact_plus_edits_plus_nn_vote",
            "max_distance": 2,
            "seed": seed,
            "holdout_frac": holdout_frac,
            "n_pairs_total": len(pairs),
            "n_train": len(subset),
            "n_holdout": n_holdout,
            "lookup": lookup,
            "memory": memory,
            "edits": learn_edits(subset, min_count=1),
        }

    holdout_srcs = {norm_key(p["src"]) for p in holdout}
    model = pack(pairs, n_holdout=len(holdout), holdout_srcs=set())
    model["eval_train_size"] = len(train)
    model_path.write_text(json.dumps(model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    fold_path = model_path.with_name("normalizer_model_trainfold.json")
    fold_path.write_text(
        json.dumps(
            pack(train, n_holdout=len(holdout), holdout_srcs=holdout_srcs),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    with heldout_path.open("w", encoding="utf-8") as f:
        for p in holdout:
            f.write(
                json.dumps(
                    {"input": p["src"], "expected": p["tgt"], "entry_id": p["entry_id"]},
                    ensure_ascii=False,
                )
                + "\n"
            )
    return model


def load_model(path: Path = MODEL_PATH) -> dict:
    if not path.is_file():
        raise FileNotFoundError(
            f"Missing {path}. Run: python data/normalize.py --train"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def load_train_fold(path: Path | None = None) -> dict:
    path = path or MODEL_PATH.with_name("normalizer_model_trainfold.json")
    if not path.is_file():
        raise FileNotFoundError(f"Missing {path}. Run: python data/normalize.py --train")
    return json.loads(path.read_text(encoding="utf-8"))


def _known_targets(model: dict) -> set[str]:
    known = {norm_key(t) for t in (model.get("lookup") or {}).values()}
    for row in model.get("memory") or []:
        known.add(norm_key(row["tgt"]))
    return known


def model_resolve(core: str, model: dict) -> dict:
    """Exact lookup → edit-to-known-SNO → NN vote. Never corrupts known SNO forms."""
    if not core:
        return {"input": core, "output": core, "method": "identity", "entry_id": None}

    nk = norm_key(core)
    lookup: dict = model.get("lookup") or {}
    if nk in lookup:
        tgt = lookup[nk]
        method = "identity" if norm_key(tgt) == nk else "model_exact"
        return {"input": core, "output": tgt, "method": method, "entry_id": None}

    known_tgt = _known_targets(model)
    if nk in known_tgt:
        return {"input": core, "output": core, "method": "identity", "entry_id": None}

    edited = apply_edits(nk, model.get("edits") or [], known_tgt)
    if edited is not None:
        # Prefer canonical casing from a memory row if present
        out = edited
        for row in model.get("memory") or []:
            if norm_key(row["tgt"]) == edited:
                out = row["tgt"]
                break
        return {"input": core, "output": out, "method": "model_edit", "entry_id": None}

    max_d = int(model.get("max_distance", 2))
    if len(nk) < 2:
        return {"input": core, "output": core, "method": "unknown", "entry_id": None}

    scores: dict[str, float] = {}
    best_d_for: dict[str, int] = {}
    for row in model.get("memory") or []:
        src = row["src"]
        if abs(len(src) - len(nk)) > max_d:
            continue
        d = levenshtein(nk, src)
        if 0 < d <= max_d:
            tgt = row["tgt"]
            scores[tgt] = scores.get(tgt, 0.0) + 1.0 / d
            prev = best_d_for.get(tgt, 99)
            if d < prev:
                best_d_for[tgt] = d
    if not scores:
        return {"input": core, "output": core, "method": "unknown", "entry_id": None}

    tgt = max(scores.keys(), key=lambda t: (scores[t], -best_d_for[t], -len(t), t))
    return {"input": core, "output": tgt, "method": "model_nn", "entry_id": None}
