#!/usr/bin/env python3
"""Sentence normalizer: informal tokens → IFRA SNO.

Part II: rules (II-1) + trained exact/1-NN model (II-2). Does not write dictionary.json.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICT_PATH = ROOT / "data" / "dictionary.json"
INDEX_PATH = ROOT / "data" / "variant_index.json"
FUZZY_PATH = ROOT / "data" / "fuzzy_lookup.json"
HELDOUT_PATH = ROOT / "data" / "normalizer_heldout.jsonl"

# Word core + optional internal hyphen/apostrophe (same family as collect_variants).
WORD_RE = re.compile(
    r"[a-zA-ZàáèéìíòóùúÀÁÈÉÌÍÒÓÙÚ]+(?:[-'][a-zA-ZàáèéìíòóùúÀÁÈÉÌÍÒÓÙÚ]+)*"
)

# Gold sentences for --self-check (exact index hits — matches live variant_index).
GOLD = [
    ("Di pickin wan book.", "di pikin wan buk."),
    ("I wan book.", "I wan buk."),
    ("Yu sabi wetin?", "yu sabi wetin?"),
]


def norm_key(s: str) -> str:
    return unicodedata.normalize("NFC", s).casefold()


def load_assets() -> tuple[dict[str, str], dict[str, str], list[tuple[str, str]], int]:
    """casefold index → entry_id, id→standard_spelling, fuzzy (term,id) list, max_distance."""
    entries = json.loads(DICT_PATH.read_text(encoding="utf-8"))
    raw_index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    fuzzy_doc = json.loads(FUZZY_PATH.read_text(encoding="utf-8"))
    by_id = {e["id"]: e["standard_spelling"] for e in entries}
    index: dict[str, str] = {}
    for k, v in raw_index.items():
        nk = norm_key(k)
        if nk not in index:
            index[nk] = v
    terms = [(t["term"], t["id"]) for t in fuzzy_doc.get("terms", [])]
    max_d = int(fuzzy_doc.get("max_distance", 2))
    return index, by_id, terms, max_d


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


def resolve_token_rules(
    core: str,
    index: dict[str, str],
    by_id: dict[str, str],
    fuzzy_terms: list[tuple[str, str]],
    max_d: int,
) -> dict:
    if not core:
        return {"input": core, "output": core, "method": "identity", "entry_id": None}

    eid = index.get(norm_key(core))
    if eid is not None:
        std = by_id.get(eid, core)
        method = "identity" if norm_key(std) == norm_key(core) else "exact"
        return {"input": core, "output": std, "method": method, "entry_id": eid}

    nq = norm_key(core)
    # Fuzzy on 1–2 letter tokens is almost always English residue noise (be→bed).
    if len(nq) <= 2:
        return {"input": core, "output": core, "method": "unknown", "entry_id": None}

    # 3-letter: same-length edits only, max distance 1 (bok→buk; not be-length traps).
    lim = 1 if len(nq) <= 3 else max_d

    best: list[tuple[int, str, str]] = []
    for term, tid in fuzzy_terms:
        nt = norm_key(term)
        if abs(len(nt) - len(nq)) > lim:
            continue
        if len(nq) <= 3 and len(nt) != len(nq):
            continue
        d = levenshtein(nq, nt)
        if 0 < d <= lim:
            best.append((d, term, tid))
    if not best:
        return {"input": core, "output": core, "method": "unknown", "entry_id": None}

    best.sort(key=lambda x: (x[0], x[1].casefold()))
    _d, _term, tid = best[0]
    std = by_id.get(tid, core)
    return {"input": core, "output": std, "method": "fuzzy", "entry_id": tid}


def split_edge(raw: str) -> tuple[str, str, str]:
    if not raw:
        return "", "", ""
    m = WORD_RE.search(raw)
    if not m:
        return "", raw, ""
    return raw[: m.start()], m.group(0), raw[m.end() :]


def normalize_sentence(
    text: str,
    *,
    backend: str = "rules",
    index: dict[str, str] | None = None,
    by_id: dict[str, str] | None = None,
    fuzzy_terms: list[tuple[str, str]] | None = None,
    max_d: int | None = None,
    model: dict | None = None,
) -> dict:
    if backend == "rules":
        if index is None or by_id is None or fuzzy_terms is None or max_d is None:
            index, by_id, fuzzy_terms, max_d = load_assets()
    elif backend == "model":
        if model is None:
            from normalizer_model import load_model

            model = load_model()
    else:
        raise ValueError(f"unknown backend: {backend}")

    parts = re.split(r"(\s+)", text)
    decisions: list[dict] = []
    out_parts: list[str] = []

    for part in parts:
        if part == "" or part.isspace():
            out_parts.append(part)
            continue
        lead, core, trail = split_edge(part)
        if not core or not WORD_RE.fullmatch(core):
            out_parts.append(part)
            decisions.append(
                {"input": part, "output": part, "method": "identity", "entry_id": None}
            )
            continue
        if backend == "rules":
            dec = resolve_token_rules(core, index, by_id, fuzzy_terms, max_d)
        else:
            from normalizer_model import model_resolve

            dec = model_resolve(core, model)
        decisions.append(dec)
        out_parts.append(f"{lead}{dec['output']}{trail}")

    return {
        "input": text,
        "output": "".join(out_parts),
        "tokens": decisions,
        "backend": backend,
    }


def self_check() -> int:
    index, by_id, fuzzy_terms, max_d = load_assets()
    failed = 0
    for src, want in GOLD:
        got = normalize_sentence(
            src, backend="rules", index=index, by_id=by_id, fuzzy_terms=fuzzy_terms, max_d=max_d
        )["output"]
        if got != want:
            print(f"FAIL: {src!r}\n  got:  {got!r}\n  want: {want!r}", file=sys.stderr)
            failed += 1
        else:
            print(f"OK: {src!r} -> {got!r}")
    if failed:
        print(f"{failed} gold sentence(s) failed", file=sys.stderr)
        return 1
    print(f"self-check passed ({len(GOLD)} sentences)")
    return 0


def load_eval_rows(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def eval_backend(backend: str, rows: list[dict], model: dict | None = None) -> dict:
    assets = None
    if backend == "rules":
        assets = load_assets()
    word_ok = 0
    sent_ok = 0
    n = len(rows)
    for row in rows:
        src = row["input"]
        want = row["expected"]
        if backend == "rules":
            index, by_id, fuzzy_terms, max_d = assets
            got = normalize_sentence(
                src,
                backend="rules",
                index=index,
                by_id=by_id,
                fuzzy_terms=fuzzy_terms,
                max_d=max_d,
            )["output"]
        else:
            got = normalize_sentence(src, backend="model", model=model)["output"]
        # Token eval: strip outer punct for fair word accuracy on single-token rows
        got_core = got
        want_core = want
        m = WORD_RE.search(got)
        if m:
            got_core = m.group(0)
        m2 = WORD_RE.search(want)
        if m2:
            want_core = m2.group(0)
        if norm_key(got_core) == norm_key(want_core):
            word_ok += 1
        if norm_key(got) == norm_key(want):
            sent_ok += 1
    return {
        "backend": backend,
        "n": n,
        "word_accuracy": (word_ok / n) if n else 0.0,
        "sentence_exact": (sent_ok / n) if n else 0.0,
        "word_ok": word_ok,
        "sent_ok": sent_ok,
    }


def print_metrics(m: dict) -> None:
    print(
        f"{m['backend']}: n={m['n']}  word_acc={m['word_accuracy']:.3f} "
        f"({m['word_ok']}/{m['n']})  sent_exact={m['sentence_exact']:.3f} "
        f"({m['sent_ok']}/{m['n']})"
    )


def main(argv: list[str] | None = None) -> int:
    # Allow `python data/normalize.py` to import sibling module
    sys.path.insert(0, str(Path(__file__).resolve().parent))

    p = argparse.ArgumentParser(
        description="Normalize informal Naija sentence to SNO (rules or model)."
    )
    p.add_argument("text", nargs="?", help="Sentence to normalize")
    p.add_argument("--json", action="store_true", help="Emit full decision JSON")
    p.add_argument("--self-check", action="store_true", help="Run gold sentence checks (rules)")
    p.add_argument(
        "--backend",
        choices=("rules", "model"),
        default="rules",
        help="Normalizer backend (default: rules)",
    )
    p.add_argument(
        "--train",
        action="store_true",
        help="Train model from curated pairs; write normalizer_model.json + heldout",
    )
    p.add_argument(
        "--eval",
        metavar="PATH",
        nargs="?",
        const=str(HELDOUT_PATH),
        help="Eval backend on JSONL (default: data/normalizer_heldout.jsonl)",
    )
    p.add_argument(
        "--compare",
        action="store_true",
        help="Eval rules and model on the same held-out JSONL (implies --eval default)",
    )
    args = p.parse_args(argv)

    if args.train:
        from normalizer_model import train_model

        model = train_model()
        print(
            f"Trained: {model['n_pairs_total']} pairs in production model; "
            f"holdout={model['n_holdout']} (fold train={model.get('eval_train_size')}) "
            f"-> data/normalizer_model.json"
        )
        return 0

    if args.compare:
        eval_path = Path(args.eval) if args.eval else HELDOUT_PATH
        if not eval_path.is_file():
            print(f"Missing {eval_path}. Run --train first.", file=sys.stderr)
            return 1
        from normalizer_model import load_train_fold

        rows = load_eval_rows(eval_path)
        fold = load_train_fold()
        print_metrics(eval_backend("rules", rows))
        # Generalization: model fold that never saw held-out src forms
        m = eval_backend("model", rows, model=fold)
        m["backend"] = "model_fold"
        print_metrics(m)
        return 0

    if args.eval is not None:
        eval_path = Path(args.eval)
        if not eval_path.is_file():
            print(f"Missing {eval_path}. Run --train first.", file=sys.stderr)
            return 1
        rows = load_eval_rows(eval_path)
        model = None
        if args.backend == "model":
            from normalizer_model import load_model

            model = load_model()
        print_metrics(eval_backend(args.backend, rows, model=model))
        return 0

    if args.self_check:
        return self_check()

    if not args.text:
        p.print_help()
        return 2

    model = None
    if args.backend == "model":
        from normalizer_model import load_model

        model = load_model()
    result = normalize_sentence(args.text, backend=args.backend, model=model)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["output"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
