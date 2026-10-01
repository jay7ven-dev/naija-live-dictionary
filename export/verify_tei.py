#!/usr/bin/env python3
"""Verify TEI Lex-0 export exists and matches dictionary entry count."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from defusedxml import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}


def main() -> int:
    dict_path = ROOT / "data" / "dictionary.json"
    tei_path = ROOT / "export" / "naija-dictionary.lex0.xml"
    if not tei_path.is_file():
        print(f"missing: {tei_path}", file=sys.stderr)
        return 1
    entries = json.loads(dict_path.read_text(encoding="utf-8"))
    tree = ET.parse(tei_path)
    xml_entries = tree.findall(".//tei:entry", TEI_NS)
    if len(xml_entries) != len(entries):
        print(f"count mismatch: xml={len(xml_entries)} json={len(entries)}", file=sys.stderr)
        return 1
    print(f"OK: TEI Lex-0 export valid ({len(entries)} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
