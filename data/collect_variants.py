#!/usr/bin/env python3
"""Extract variant candidates from corpus and apply approved mappings to dictionary."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = ROOT / "data" / "corpus"
SOURCES = CORPUS_DIR / "sources.json"
DICT_PATH = ROOT / "data" / "dictionary.json"
CANDIDATES_PATH = ROOT / "data" / "candidates.json"
SUGGESTIONS_PATH = ROOT / "data" / "suggestions.json"
MAPPINGS_PATH = ROOT / "data" / "variant_mappings.json"
INDEX_PATH = ROOT / "data" / "variant_index.json"
FUZZY_PATH = ROOT / "data" / "fuzzy_lookup.json"

TOKEN = re.compile(
    r"[a-zA-ZàáèéìíòóùúÀÁÈÉÌÍÒÓÙÚ]+(?:[-'][a-zA-ZàáèéìíòóùúÀÁÈÉÌÍÒÓÙÚ]+)*"
)
# CENCOS-style turn labels (SPEAKER1:, Speaker2, …) — not lexical variants
SPEAKER_LABEL = re.compile(r"\bspeaker\d*\b", re.IGNORECASE)


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def norm_key(s: str) -> str:
    return s.casefold()


def load_dictionary() -> list[dict]:
    return load_json(DICT_PATH)


def build_known_index(entries: list[dict]) -> dict[str, str]:
    """norm_variant -> entry_id"""
    idx: dict[str, str] = {}
    for e in entries:
        eid = e["id"]
        idx[norm_key(e["standard_spelling"])] = eid
        for v in e.get("informal_variants", []):
            idx[norm_key(v)] = eid
    return idx


def entry_by_id(entries: list[dict]) -> dict[str, dict]:
    return {e["id"]: e for e in entries}


def corpus_files() -> list[Path]:
    manifest = load_json(SOURCES)
    paths: list[Path] = []
    for src in manifest.get("sources", []):
        rel = src.get("path", "")
        p = CORPUS_DIR / rel
        if p.is_file():
            paths.append(p)
    if not paths:
        paths = sorted(CORPUS_DIR.rglob("*.txt"))
    return paths


def extract_corpus_files() -> list[Path]:
    """Sources for variant candidate extract.

    Skip .conllu: UD_Naija-NSC is registered for example enrichment only.
    Raw CoNLL-U dumps MISC/metadata (AlignBegin, Gloss, …) into token counts.
    """
    return [p for p in corpus_files() if p.suffix.lower() != ".conllu"]


def tokenize(text: str) -> list[str]:
    text = SPEAKER_LABEL.sub(" ", text)
    tokens = TOKEN.findall(text)
    out = list(tokens)
    # bigrams ending in dem (e.g. pickin dem, people-dem already single token if hyphenated)
    for i in range(len(tokens) - 1):
        if tokens[i + 1].casefold() == "dem":
            out.append(f"{tokens[i]} dem")
            if "-" not in tokens[i]:
                out.append(f"{tokens[i]}-dem")
    return out


def cmd_extract() -> int:
    entries = load_dictionary()
    known = build_known_index(entries)
    counts: Counter[str] = Counter()
    by_source: dict[str, Counter[str]] = {}
    files = extract_corpus_files()

    for path in files:
        text = path.read_text(encoding="utf-8")
        toks = tokenize(text)
        rel = str(path.relative_to(CORPUS_DIR))
        by_source[rel] = Counter(toks)
        counts.update(toks)

    candidates = []
    for token, count in counts.most_common():
        key = norm_key(token)
        status = "known"
        entry_id = known.get(key)
        if not entry_id:
            status = "unmatched"
        candidates.append(
            {
                "token": token,
                "count": count,
                "status": status,
                "entry_id": entry_id,
                "sources": [rel for rel, c in by_source.items() if c[token] > 0],
            }
        )

    unmatched = sum(1 for c in candidates if c["status"] == "unmatched")
    save_json(
        CANDIDATES_PATH,
        {
            "generated_from": [str(p.relative_to(ROOT)) for p in files],
            "total_tokens": sum(counts.values()),
            "unique_tokens": len(counts),
            "unmatched_count": unmatched,
            "candidates": candidates,
        },
    )
    print(f"Extracted {len(counts)} unique tokens ({unmatched} unmatched) -> {CANDIDATES_PATH}")
    return 0


def cmd_apply() -> int:
    entries = load_dictionary()
    by_id = entry_by_id(entries)
    data = load_json(MAPPINGS_PATH)
    added = 0
    skipped = 0

    for m in data.get("mappings", []):
        variant = m["variant"]
        eid = m["entry_id"]
        if eid not in by_id:
            print(f"skip: unknown entry_id {eid!r} for variant {variant!r}", file=sys.stderr)
            skipped += 1
            continue
        entry = by_id[eid]
        std = entry["standard_spelling"]
        if norm_key(variant) == norm_key(std):
            skipped += 1
            continue
        variants = entry.setdefault("informal_variants", [])
        if any(norm_key(v) == norm_key(variant) for v in variants):
            skipped += 1
            continue
        variants.append(variant)
        added += 1

    save_json(DICT_PATH, entries)
    print(f"Applied {added} new variants ({skipped} skipped) -> {DICT_PATH}")
    return 0


def cmd_index() -> int:
    entries = load_dictionary()
    index: dict[str, str] = {}

    # Approved mappings win over ambiguous dictionary variants
    mappings = load_json(MAPPINGS_PATH).get("mappings", [])
    for m in mappings:
        variant = m["variant"]
        eid = m["entry_id"]
        if variant not in index:
            index[variant] = eid

    for e in entries:
        eid = e["id"]
        std = e["standard_spelling"]
        if std not in index:
            index[std] = eid
        for v in e.get("informal_variants", []):
            if v not in index:
                index[v] = eid
    save_json(INDEX_PATH, index)

    fuzzy_terms = [{"term": term, "id": eid} for term, eid in sorted(index.items(), key=lambda x: x[0].casefold())]
    save_json(
        FUZZY_PATH,
        {
            "max_distance": 2,
            "generated_from": str(INDEX_PATH.relative_to(ROOT)),
            "terms": fuzzy_terms,
        },
    )
    print(f"Wrote {len(index)} lookup keys -> {INDEX_PATH}")
    print(f"Wrote {len(fuzzy_terms)} fuzzy terms -> {FUZZY_PATH}")
    return 0


def cmd_suggest() -> int:
    """Lin/FST-inspired variant suggestions for unmatched corpus tokens (human review only)."""
    try:
        from fst_variants import suggest_entry_for_token, fst_available

        engine = "fst" if fst_available() else "lin"
    except ImportError:
        from lin_variants import suggest_entry_for_token

        engine = "lin"

    entries = load_dictionary()
    standards = [(e["id"], e["standard_spelling"]) for e in entries]
    known = build_known_index(entries)

    if CANDIDATES_PATH.is_file():
        cand_data = load_json(CANDIDATES_PATH)
        pool = [c for c in cand_data.get("candidates", []) if c.get("status") == "unmatched"]
    else:
        print("No candidates.json — run extract first", file=sys.stderr)
        return 1

    suggestions = []
    for c in pool:
        token = c["token"]
        if norm_key(token) in known:
            continue
        hit = suggest_entry_for_token(token, standards)
        if not hit:
            continue
        eid, method = hit
        std = entry_by_id(entries)[eid]["standard_spelling"]
        suggestions.append(
            {
                "variant": token,
                "count": c.get("count", 0),
                "suggested_entry_id": eid,
                "standard_spelling": std,
                "method": method,
                "sources": c.get("sources", []),
                "status": "pending_review",
            }
        )

    save_json(
        SUGGESTIONS_PATH,
        {
            "note": "Suggestions only — add approved rows to variant_mappings.json; never auto-applied.",
            "engine": engine,
            "count": len(suggestions),
            "suggestions": suggestions,
        },
    )
    print(f"Wrote {len(suggestions)} suggestions -> {SUGGESTIONS_PATH}")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: collect_variants.py extract|suggest|fst-suggest|apply|index", file=sys.stderr)
        return 1
    cmd = argv[1]
    if cmd == "extract":
        return cmd_extract()
    if cmd == "suggest" or cmd == "fst-suggest":
        return cmd_suggest()
    if cmd == "apply":
        return cmd_apply()
    if cmd == "index":
        return cmd_index()
    print(f"Unknown command: {cmd}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
