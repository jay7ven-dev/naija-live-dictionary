#!/usr/bin/env python3
"""Enrich dictionary example_sentences from UD_Naija-NSC (R4). CC BY-SA 4.0."""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.request import urlopen

from example_quality import passes_quality

ROOT = Path(__file__).resolve().parent.parent
DICT_PATH = ROOT / "data" / "dictionary.json"
CORPUS = ROOT / "data" / "corpus" / "external"
SOURCES = ROOT / "data" / "corpus" / "sources.json"
SUGGESTIONS_PATH = ROOT / "data" / "example_suggestions.json"

UD_BASE = "https://raw.githubusercontent.com/UniversalDependencies/UD_Naija-NSC/master/"
UD_FILES = [
    "pcm_nsc-ud-train.conllu",
    "pcm_nsc-ud-dev.conllu",
    "pcm_nsc-ud-test.conllu",
]
MAX_EXAMPLES_PER_ENTRY = 2  # disciplined A+B: primary + at most one secondary
MAX_NEW_FROM_UD = 1  # never bulk-add more than one filtered secondary

WORD = re.compile(r"[a-zA-ZàáèéìíòóùúÀÁÈÉÌÍÒÓÙÚ]+(?:[-'][a-zA-ZàáèéìíòóùúÀÁÈÉÌÍÒÓÙÚ]+)*")


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def norm(s: str) -> str:
    return unicodedata.normalize("NFC", s).casefold()


def strip_diacritics(s: str) -> str:
    nfd = unicodedata.normalize("NFD", s)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


def word_pattern(word: str) -> re.Pattern[str]:
    w = re.escape(word)
    return re.compile(rf"(?<![a-zA-Zàáèéìíòóùú'-]){w}(?![a-zA-Zàáèéìíòóùú'-])", re.IGNORECASE)


def register_ud_source() -> None:
    data = load_json(SOURCES) if SOURCES.is_file() else {"sources": []}
    sources = data.setdefault("sources", [])
    for name in UD_FILES:
        sid = f"ud-naija-{name.replace('.conllu', '')}"
        row = {
            "id": sid,
            "path": f"external/{name}",
            "source_type": "licensed_corpus",
            "license": "CC BY-SA 4.0",
            "collected": "2026-07-10",
            "notes": "UniversalDependencies/UD_Naija-NSC — example_sentences enrichment only; cite Caron et al.",
        }
        sources[:] = [s for s in sources if s.get("id") != sid]
        sources.append(row)
    save_json(SOURCES, data)


def cmd_ingest() -> int:
    CORPUS.mkdir(parents=True, exist_ok=True)
    for name in UD_FILES:
        url = UD_BASE + name
        out = CORPUS / name
        print(f"Fetching {name} …")
        with urlopen(url, timeout=300) as resp:
            out.write_bytes(resp.read())
        print(f"  -> {out} ({out.stat().st_size // 1024} KB)")
    register_ud_source()
    print("Registered UD_Naija-NSC in sources.json")
    return 0


def parse_conllu(path: Path) -> list[dict]:
    sentences: list[dict] = []
    meta: dict[str, str] = {}
    lemmas: set[str] = set()
    forms: set[str] = set()

    def flush() -> None:
        nonlocal meta, lemmas, forms
        ortho = meta.get("text_ortho") or meta.get("text")
        if ortho:
            ortho = re.sub(r"\s+", " ", ortho).strip()
            if len(ortho) >= 8:
                sentences.append(
                    {
                        "sent_id": meta.get("sent_id", ""),
                        "ortho": ortho,
                        "lemmas": set(lemmas),
                        "forms": set(forms),
                        "source_file": path.name,
                    }
                )
        meta = {}
        lemmas = set()
        forms = set()

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# sent_id = "):
            flush()
            meta["sent_id"] = line.split("=", 1)[1].strip()
            continue
        if line.startswith("# text_ortho = "):
            meta["text_ortho"] = line.split("=", 1)[1].strip()
            continue
        if line.startswith("# text = ") and "text_ortho" not in meta:
            meta["text"] = line.split("=", 1)[1].strip()
            continue
        if line.startswith("#"):
            continue
        if not line.strip():
            continue
        cols = line.split("\t")
        if len(cols) < 3:
            continue
        form, lemma = cols[1], cols[2]
        if form == "#" or lemma == "_":
            continue
        forms.add(norm(form))
        forms.add(norm(strip_diacritics(form)))
        lemmas.add(norm(lemma))
        lemmas.add(norm(strip_diacritics(lemma)))

    flush()
    return sentences


def load_all_sentences() -> list[dict]:
    paths = [CORPUS / n for n in UD_FILES if (CORPUS / n).is_file()]
    if not paths:
        raise FileNotFoundError("No CoNLL-U files — run: enrich_examples.py ingest")
    out: list[dict] = []
    for p in paths:
        out.extend(parse_conllu(p))
    return out


def entry_match_keys(entry: dict) -> list[str]:
    keys = {norm(entry["standard_spelling"]), norm(strip_diacritics(entry["standard_spelling"]))}
    keys.add(norm(entry["id"].replace("-", " ")))
    for v in entry.get("informal_variants", []):
        keys.add(norm(v))
        keys.add(norm(strip_diacritics(v)))
    return [k for k in keys if k and len(k) >= 1]


def sentence_matches_entry(sent: dict, entry: dict) -> tuple[bool, bool]:
    """Return (matched, sno_surface_in_ortho)."""
    std = entry["standard_spelling"]
    ortho = sent["ortho"]
    sno_surface = bool(word_pattern(std).search(ortho)) or bool(
        word_pattern(strip_diacritics(std)).search(strip_diacritics(ortho))
    )
    keys = entry_match_keys(entry)
    lemma_hit = bool(sent["lemmas"] & set(keys))
    form_hit = bool(sent["forms"] & set(keys))
    if sno_surface:
        return True, True
    if lemma_hit or form_hit:
        return True, False
    return False, False


def score_sentence(sent: dict, sno_surface: bool) -> int:
    n = len(sent["ortho"])
    score = 10 if sno_surface else 3
    if 25 <= n <= 100:
        score += 5
    elif n <= 120:
        score += 2
    return score


def cmd_extract() -> int:
    entries = load_json(DICT_PATH)
    sentences = load_all_sentences()
    print(f"Parsed {len(sentences)} UD sentences")

    suggestions = []
    for entry in entries:
        eid = entry["id"]
        existing = {norm(x) for x in entry.get("example_sentences", [])}
        hits: list[tuple[int, dict, bool]] = []
        for sent in sentences:
            matched, sno = sentence_matches_entry(sent, entry)
            if not matched:
                continue
            if norm(sent["ortho"]) in existing:
                continue
            hits.append((score_sentence(sent, sno), sent, sno))

        hits.sort(key=lambda x: (-x[0], x[1]["ortho"]))
        picked = []
        for _, sent, sno in hits[: MAX_NEW_FROM_UD * 3]:
            if len(picked) >= MAX_NEW_FROM_UD:
                break
            if any(norm(p["ortho"]) == norm(sent["ortho"]) for p in picked):
                continue
            picked.append({**sent, "sno_surface": sno})

        if picked:
            suggestions.append(
                {
                    "entry_id": eid,
                    "standard_spelling": entry["standard_spelling"],
                    "existing_count": len(entry.get("example_sentences", [])),
                    "candidates": [
                        {
                            "sentence": p["ortho"],
                            "sent_id": p["sent_id"],
                            "source_file": p["source_file"],
                            "sno_surface": p["sno_surface"],
                        }
                        for p in picked
                    ],
                }
            )

    save_json(
        SUGGESTIONS_PATH,
        {
            "source": "UD_Naija-NSC",
            "license": "CC BY-SA 4.0",
            "entry_count": len(suggestions),
            "suggestions": suggestions,
        },
    )
    total = sum(len(s["candidates"]) for s in suggestions)
    print(f"Wrote {len(suggestions)} entries / {total} candidate examples -> {SUGGESTIONS_PATH}")
    return 0


def cmd_apply() -> int:
    """Apply at most one filtered secondary example per entry (disciplined A+B)."""
    entries = load_json(DICT_PATH)
    if not SUGGESTIONS_PATH.is_file():
        print("Run extract first", file=sys.stderr)
        return 1
    data = load_json(SUGGESTIONS_PATH)
    by_id = {e["id"]: e for e in entries}
    added = 0
    touched = 0
    skipped = 0

    for block in data.get("suggestions", []):
        eid = block["entry_id"]
        if eid not in by_id:
            continue
        entry = by_id[eid]
        examples = list(entry.get("example_sentences", []))
        if len(examples) >= MAX_EXAMPLES_PER_ENTRY:
            continue
        existing = {norm(x) for x in examples}
        new_for_entry = 0
        for cand in block.get("candidates", []):
            if len(examples) >= MAX_EXAMPLES_PER_ENTRY:
                break
            if new_for_entry >= MAX_NEW_FROM_UD:
                break
            sent = cand["sentence"]
            if norm(sent) in existing:
                continue
            ok, reason = passes_quality(sent, entry, secondary=True)
            if not ok:
                skipped += 1
                continue
            examples.append(sent)
            existing.add(norm(sent))
            added += 1
            new_for_entry += 1
        if new_for_entry:
            entry["example_sentences"] = examples
            note = entry.get("notes", "")
            tag = "UD_Naija-NSC example (CC BY-SA 4.0)"
            if tag not in note:
                entry["notes"] = f"{note} | {tag}".strip(" |") if note else tag
            touched += 1

    save_json(DICT_PATH, entries)
    print(f"Applied {added} filtered secondary examples to {touched} entries ({skipped} rejected by quality gate) -> {DICT_PATH}")
    print("Tip: run clean_examples.py apply afterward to re-rank primary/secondary and quarantine surplus.")
    return 0


def cmd_report() -> int:
    entries = load_json(DICT_PATH)
    with_ud = sum(1 for e in entries if "UD_Naija" in (e.get("notes") or ""))
    multi = sum(1 for e in entries if len(e.get("example_sentences", [])) > 1)
    print(f"{len(entries)} entries; {multi} with 2+ examples; {with_ud} tagged UD_Naija-NSC")
    if SUGGESTIONS_PATH.is_file():
        s = load_json(SUGGESTIONS_PATH)
        print(f"Pending suggestions file: {s.get('entry_count', 0)} entries")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: enrich_examples.py ingest|extract|apply|report", file=sys.stderr)
        return 1
    cmd = argv[1]
    try:
        if cmd == "ingest":
            return cmd_ingest()
        if cmd == "extract":
            return cmd_extract()
        if cmd == "apply":
            return cmd_apply()
        if cmd == "report":
            return cmd_report()
    except Exception as exc:
        print(f"failed: {exc}", file=sys.stderr)
        return 1
    print(f"Unknown command: {cmd}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
