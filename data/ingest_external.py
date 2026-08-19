#!/usr/bin/env python3
"""Ingest licensed external PCM corpora into data/corpus/ (R3: NaijaSenti + CENCOS)."""
from __future__ import annotations

import csv
import json
import re
import sys
import zipfile
from io import BytesIO
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "corpus"
EXTERNAL = CORPUS / "external"
SOURCES = CORPUS / "sources.json"

NAIJASENTI_URLS = [
    "https://github.com/hausanlp/NaijaSenti/releases/download/v0.1.1/data.zip",
    "https://raw.githubusercontent.com/hausanlp/NaijaSenti/main/data/annotated_tweets/pcm_train.csv",
]
CENCOS_ZENODO = "https://zenodo.org/records/7314016/files/CENCOS%20corpus.zip?download=1"

TOKEN = re.compile(r"[a-zA-Zàáèéìíòóùú'-]+")


def load_sources() -> dict:
    if SOURCES.is_file():
        return json.loads(SOURCES.read_text(encoding="utf-8"))
    return {"sources": []}


def save_sources(data: dict) -> None:
    SOURCES.parent.mkdir(parents=True, exist_ok=True)
    SOURCES.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def register_source(source_id: str, path: str, notes: str) -> None:
    data = load_sources()
    sources = data.setdefault("sources", [])
    rel = path.replace("\\", "/")
    row = {
        "id": source_id,
        "path": rel,
        "source_type": "licensed_corpus",
        "license": "see source",
        "collected": "2026-07-10",
        "notes": notes,
    }
    sources[:] = [s for s in sources if s.get("id") != source_id]
    sources.append(row)
    save_sources(data)


def _lines_from_csv(raw: str) -> list[str]:
    reader = csv.DictReader(raw.splitlines())
    text_col = None
    for col in ("tweet", "text", "Tweet", "Text", "content"):
        if reader.fieldnames and col in reader.fieldnames:
            text_col = col
            break
    if not text_col:
        raise RuntimeError(f"No text column in CSV: {reader.fieldnames}")
    return [(row.get(text_col) or "").strip() for row in reader if (row.get(text_col) or "").strip()]


def _lines_from_zip(data: bytes, pcm_only: bool = True) -> list[str]:
    lines: list[str] = []
    with zipfile.ZipFile(BytesIO(data)) as zf:
        for name in zf.namelist():
            lower = name.lower()
            if pcm_only and "pcm" not in lower and not lower.endswith("pidgin"):
                if "annotated" in lower and lower.endswith(".csv"):
                    pass  # may still be multi-lang zip; filter rows below
            if not lower.endswith((".csv", ".txt")):
                continue
            content = zf.read(name).decode("utf-8", errors="replace")
            if lower.endswith(".csv"):
                reader = csv.DictReader(content.splitlines())
                lang_col = next((c for c in ("language", "lang", "Language") if reader.fieldnames and c in reader.fieldnames), None)
                text_col = next(
                    (c for c in ("tweet", "text", "Tweet", "Text", "content") if reader.fieldnames and c in reader.fieldnames),
                    None,
                )
                if not text_col:
                    continue
                for row in reader:
                    if lang_col and (row.get(lang_col) or "").casefold() not in ("pcm", "pidgin", "nigerian-pidgin", ""):
                        continue
                    t = (row.get(text_col) or "").strip()
                    if t:
                        lines.append(t)
            else:
                for line in content.splitlines():
                    line = line.strip()
                    if line:
                        lines.append(line)
    return lines


def _lines_from_hf_datasets_lib() -> list[str]:
    from datasets import load_dataset

    ds = load_dataset("HausaNLP/NaijaSenti-Twitter", "pcm", split="train")
    col = "text" if "text" in ds.column_names else "tweet"
    return [str(row[col]).strip() for row in ds if str(row[col]).strip()]


def _lines_from_hf_pcm(max_rows: int = 6000) -> list[str]:
    """Paginate Hugging Face datasets server for pcm train tweets."""
    lines: list[str] = []
    offset = 0
    page = 500
    while offset < max_rows:
        length = min(page, max_rows - offset)
        url = (
            "https://datasets-server.huggingface.co/rows?"
            f"dataset={quote('HausaNLP/NaijaSenti-Twitter')}&config=pcm&split=train"
            f"&offset={offset}&length={length}"
        )
        req = Request(url, headers={"User-Agent": "pidgin-dictionary-ingest/1.0"})
        with urlopen(req, timeout=120) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        rows = payload.get("rows") or []
        if not rows:
            break
        for row in rows:
            cells = row.get("row") or {}
            text = (cells.get("text") or cells.get("tweet") or "").strip()
            if text:
                lines.append(text)
        offset += len(rows)
        if len(rows) < length:
            break
    return lines


def ingest_naijasenti() -> int:
    EXTERNAL.mkdir(parents=True, exist_ok=True)
    out = EXTERNAL / "naijasenti-pcm-train.txt"
    lines: list[str] = []
    last_err: Exception | None = None

    try:
        print("Trying Hugging Face datasets library …")
        lines = _lines_from_hf_datasets_lib()
        if lines:
            print(f"  got {len(lines)} tweets via datasets")
    except Exception as exc:
        last_err = exc
        print(f"  datasets skip: {exc}", file=sys.stderr)

    if not lines:
        try:
            print("Fetching NaijaSenti pcm train via Hugging Face datasets server …")
            lines = _lines_from_hf_pcm()
            if lines:
                print(f"  got {len(lines)} tweets from HF server")
        except (HTTPError, URLError, json.JSONDecodeError) as exc:
            last_err = exc
            print(f"  HF server skip: {exc}", file=sys.stderr)

    if not lines:
        for url in NAIJASENTI_URLS:
            try:
                print(f"Fetching NaijaSenti from {url} …")
                with urlopen(url, timeout=180) as resp:
                    data = resp.read()
                if url.endswith(".zip"):
                    lines = _lines_from_zip(data, pcm_only=True)
                else:
                    lines = _lines_from_csv(data.decode("utf-8", errors="replace"))
                if lines:
                    break
            except (HTTPError, URLError, RuntimeError, zipfile.BadZipFile) as exc:
                last_err = exc
                print(f"  skip: {exc}", file=sys.stderr)
    if not lines:
        raise RuntimeError(f"NaijaSenti ingest failed: {last_err}")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    register_source(
        "naijasenti-pcm-train",
        "external/naijasenti-pcm-train.txt",
        "HausaNLP/NaijaSenti — variant mining only; cite Muhammad et al. 2022.",
    )
    print(f"Wrote {len(lines)} lines -> {out}")
    return len(lines)


def ingest_cencos() -> int:
    EXTERNAL.mkdir(parents=True, exist_ok=True)
    out = EXTERNAL / "cencos-transcripts.txt"
    print("Fetching CENCOS zip from Zenodo …")
    with urlopen(CENCOS_ZENODO, timeout=180) as resp:
        data = resp.read()
    texts: list[str] = []
    with zipfile.ZipFile(BytesIO(data)) as zf:
        for name in zf.namelist():
            if name.lower().endswith((".txt", ".csv")) and "speaker" not in name.lower():
                try:
                    content = zf.read(name).decode("utf-8", errors="replace")
                except Exception:
                    continue
                if name.lower().endswith(".csv"):
                    reader = csv.reader(content.splitlines())
                    for row in reader:
                        texts.extend(TOKEN.findall(" ".join(row)))
                else:
                    texts.append(content)
    merged = "\n\n".join(texts) if texts else ""
    if not merged.strip():
        raise RuntimeError("CENCOS zip contained no usable text files")
    out.write_text(merged, encoding="utf-8")
    register_source(
        "cencos-zenodo",
        "external/cencos-transcripts.txt",
        "Zenodo 7314016 CENCOS — text only; cite Agbo & Plag 2022.",
    )
    print(f"Wrote CENCOS text -> {out}")
    return len(merged.split())


def main(argv: list[str]) -> int:
    which = argv[1] if len(argv) > 1 else "all"
    errors: list[str] = []
    if which in ("naijasenti", "all"):
        try:
            ingest_naijasenti()
        except Exception as exc:
            errors.append(f"naijasenti: {exc}")
    if which in ("cencos", "all"):
        try:
            ingest_cencos()
        except Exception as exc:
            errors.append(f"cencos: {exc}")
    if errors:
        for e in errors:
            print(f"ingest failed: {e}", file=sys.stderr)
        print("Manual fallback: place .txt under data/corpus/external/ and register in sources.json", file=sys.stderr)
        return 1
    print("Done. Run: python data/collect_variants.py extract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
