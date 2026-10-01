#!/usr/bin/env python3
"""Build a D4 Tier A/B offline zip (no IFRA guide body, no full corpus dumps)."""
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

# Paths relative to ROOT — Tier A/B only (see docs/d4-public-release-licensing.md).
INCLUDE_FILES = [
    "LICENSE",
    "README.md",
    "PROJECT.md",
    "data/dictionary.json",
    "data/variant_index.json",
    "data/fuzzy_lookup.json",
    "data/variant_mappings.json",
    "data/corpus/sources.json",
    "data/ime/naija-ime-lexicon.json",
    "data/ime/naija-ime-lexicon.tsv",
    "data/ime/README.md",
    "data/last_grown.json",
    "data/eval/messy_pidgin_sample.jsonl",
    "data/eval/coverage_baseline.json",
    "export/naija-dictionary.lex0.xml",
    "export/tei_lex0.py",
    "export/verify_tei.py",
    "docs/citation-pack.md",
    "docs/d4-public-release-licensing.md",
    "docs/public-release-checklist.md",
    "docs/manuscripts/naija-live-dictionary.md",
    "docs/CANONICAL.md",
    "schema/entry.schema.json",
    "schema/validate.py",
    "web/serve.py",
    "web/verify.py",
    "web/index.html",
    "web/app.js",
    "web/style.css",
    "web/normalize.html",
    "web/normalize.js",
    "data/last_grown.json",
    "ime/keyman/naija_sno/naija_sno.kmn",
    "ime/keyman/naija_sno/naija_sno.kps",
    "ime/keyman/naija_sno/naija_sno.wordlist.tsv",
    "ime/keyman/naija_sno/README.md",
    "ime/keyman/naija_sno/readme.txt",
]

INCLUDE_GLOBS = [
    "web/docs/**/*.html",
    "web/docs/**/*.css",
    "data/*.py",
    "schema/*.json",
]

# Never ship these classes (D4 Tier C / D3 dumps / local junk).
BLOCK_SUFFIXES = (".pdf", ".conllu", ".kmx", ".kmp")
BLOCK_NAMES = {
    "cencos-transcripts.txt",
    "ifra-guide.pdf",
}


NOTICE = """Naijá Live Dictionary — D4 Tier A/B offline package
=====================================================

Orthography follows the IFRA/NLA Standard Naijá Orthography (2010).
This project is not affiliated with IFRA Nigeria.
See docs/citation-pack.md and docs/d4-public-release-licensing.md.

This zip excludes:
- IFRA Guide PDF / long verbatim guide text (Tier C)
- Full third-party corpus dumps (UD .conllu, CENCOS transcripts)
- Keyman compiled binaries (.kmx / .kmp); rebuild locally if needed

Run: python web/serve.py  →  http://localhost:8765/web/normalize.html (Fix spelling)
Dictionary: http://localhost:8765/web/index.html
"""


def collect_paths() -> list[Path]:
    out: list[Path] = []
    seen: set[Path] = set()

    def add(p: Path) -> None:
        if not p.is_file():
            return
        if p.suffix.lower() in BLOCK_SUFFIXES or p.name in BLOCK_NAMES:
            return
        rel = p.resolve()
        if rel in seen:
            return
        seen.add(rel)
        out.append(p)

    for rel in INCLUDE_FILES:
        add(ROOT / rel)
    for pattern in INCLUDE_GLOBS:
        for p in ROOT.glob(pattern):
            add(p)
    return sorted(out, key=lambda p: p.as_posix().lower())


def build_zip(out: Path) -> tuple[int, list[str]]:
    paths = collect_paths()
    missing = [rel for rel in INCLUDE_FILES if not (ROOT / rel).is_file()]
    DIST.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("NOTICE.txt", NOTICE)
        meta = {
            "package": "naija-live-dictionary-tier-ab",
            "date": date.today().isoformat(),
            "d4": "Tier A + B",
            "entry_count_hint": "see data/dictionary.json",
            "file_count": len(paths),
        }
        # live entry count if dictionary present
        dict_path = ROOT / "data" / "dictionary.json"
        if dict_path.is_file():
            meta["entries"] = len(json.loads(dict_path.read_text(encoding="utf-8")))
        zf.writestr("PACKAGE.json", json.dumps(meta, indent=2) + "\n")
        for p in paths:
            arc = p.relative_to(ROOT).as_posix()
            zf.write(p, arcname=arc)
    return len(paths), missing


def self_check(out: Path) -> int:
    errors: list[str] = []
    if not out.is_file():
        errors.append(f"missing {out}")
        return 1
    with zipfile.ZipFile(out, "r") as zf:
        names = zf.namelist()
        if "NOTICE.txt" not in names:
            errors.append("NOTICE.txt missing from zip")
        for n in names:
            lower = n.lower()
            if lower.endswith(BLOCK_SUFFIXES) or Path(n).name in BLOCK_NAMES:
                errors.append(f"blocked path in zip: {n}")
            if "cencos-transcripts" in lower or "/external/" in lower.replace("\\", "/"):
                if n.endswith((".conllu", ".txt")) and "sources.json" not in n:
                    errors.append(f"corpus dump in zip: {n}")
    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1
    print(f"OK: {out.name} ({out.stat().st_size} bytes), {len(names)} members")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Package D4 Tier A/B offline zip.")
    p.add_argument("--self-check", action="store_true", help="Validate an existing or freshly built zip")
    p.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output zip path (default: dist/naija-live-dictionary-tier-ab-YYYY-MM-DD.zip)",
    )
    args = p.parse_args(argv)
    out = args.output or (DIST / f"naija-live-dictionary-tier-ab-{date.today().isoformat()}.zip")
    if not args.self_check or not out.is_file():
        n, missing = build_zip(out)
        print(f"Wrote {n} files -> {out.relative_to(ROOT)}")
        if missing:
            print("WARN: listed but missing on disk:", ", ".join(missing), file=sys.stderr)
    return self_check(out)


if __name__ == "__main__":
    raise SystemExit(main())
