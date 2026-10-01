#!/usr/bin/env python3
"""Populate optional pronunciation field (R6 / Phase 5c)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
DICT_PATH = ROOT / "data" / "dictionary.json"
CORPUS = ROOT / "data" / "corpus" / "external"
SOURCES = ROOT / "data" / "corpus" / "sources.json"
CV_OUT = CORPUS / "common-voice-pcm-sentences.txt"

TOKEN = re.compile(r"[a-zA-Zàáèéìíòóùú'-]+")


def _urlopen(url_or_req, timeout: float):
    """urlopen restricted to http(s) (bandit B310)."""
    url = url_or_req.full_url if isinstance(url_or_req, Request) else str(url_or_req)
    scheme = urlparse(url).scheme.lower()
    if scheme not in ("http", "https"):
        raise ValueError(f"refusing non-http(s) URL scheme: {scheme!r}")
    return urlopen(url_or_req, timeout=timeout)  # nosec B310 — scheme checked above


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def register_cv_source() -> None:
    data = load_json(SOURCES) if SOURCES.is_file() else {"sources": []}
    sources = data.setdefault("sources", [])
    row = {
        "id": "common-voice-pcm",
        "path": "external/common-voice-pcm-sentences.txt",
        "source_type": "licensed_corpus",
        "license": "CC0",
        "collected": "2026-07-10",
        "notes": "Mozilla Common Voice pcm validated sentences — pronunciation/example enrichment.",
    }
    sources[:] = [s for s in sources if s.get("id") != "common-voice-pcm"]
    sources.append(row)
    save_json(SOURCES, data)


def ingest_common_voice(max_rows: int = 800) -> int:
    """Fetch pcm validated sentences via Hugging Face datasets server."""
    CORPUS.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    offset = 0
    page = 200
    while offset < max_rows:
        length = min(page, max_rows - offset)
        url = (
            "https://datasets-server.huggingface.co/rows?"
            f"dataset={quote('mozilla-foundation/common_voice_17_0')}&config=pcm&split=validated"
            f"&offset={offset}&length={length}"
        )
        req = Request(url, headers={"User-Agent": "pidgin-dictionary-ingest/1.0"})
        with _urlopen(req, timeout=120) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        rows = payload.get("rows") or []
        if not rows:
            break
        for row in rows:
            cells = row.get("row") or {}
            text = (cells.get("sentence") or cells.get("text") or "").strip()
            if text:
                lines.append(text)
        offset += len(rows)
        if len(rows) < length:
            break
    if not lines:
        raise RuntimeError("Common Voice pcm fetch returned no sentences")
    CV_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    register_cv_source()
    print(f"Wrote {len(lines)} CV sentences -> {CV_OUT}")
    return len(lines)


def cmd_apply(only_missing: bool = True) -> int:
    from g2p_hints import broad_pronunciation

    entries = load_json(DICT_PATH)
    added = 0
    for entry in entries:
        if only_missing and entry.get("pronunciation"):
            continue
        hint = broad_pronunciation(entry["standard_spelling"])
        if hint:
            entry["pronunciation"] = hint
            added += 1
    save_json(DICT_PATH, entries)
    print(f"Applied {added} pronunciation hints -> {DICT_PATH}")
    return 0


def cmd_report() -> int:
    entries = load_json(DICT_PATH)
    with_pron = sum(1 for e in entries if e.get("pronunciation"))
    print(f"{with_pron}/{len(entries)} entries have pronunciation")
    if CV_OUT.is_file():
        lines = CV_OUT.read_text(encoding="utf-8").strip().splitlines()
        print(f"Common Voice corpus: {len(lines)} sentences at {CV_OUT}")
    return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] in {"-h", "--help"}:
        print("Usage: enrich_pronunciation.py apply|ingest-cv|report", file=sys.stderr)
        return 1
    cmd = argv[0]
    if cmd == "apply":
        return cmd_apply()
    if cmd == "report":
        return cmd_report()
    if cmd == "ingest-cv":
        try:
            ingest_common_voice()
        except (HTTPError, URLError, RuntimeError) as exc:
            print(f"ingest-cv failed: {exc}", file=sys.stderr)
            print("Optional: pip install datasets; place CV pcm .txt under data/corpus/external/", file=sys.stderr)
            return 1
        return 0
    print(f"Unknown command: {cmd}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
