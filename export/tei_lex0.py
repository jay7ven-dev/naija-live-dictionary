#!/usr/bin/env python3
"""Export dictionary.json to TEI Lex-0 XML (R5 / Phase 5b). JSON remains canonical."""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
DICT_PATH = ROOT / "data" / "dictionary.json"
DEFAULT_OUT = ROOT / "export" / "naija-dictionary.lex0.xml"

TEI_NS = "http://www.tei-c.org/ns/1.0"
XML_NS = "http://www.w3.org/XML/1998/namespace"
ET.register_namespace("", TEI_NS)


def _sub(parent: ET.Element, tag: str, text: str | None = None, **attrs: str) -> ET.Element:
    attrib = {}
    for k, v in attrs.items():
        if not v:
            continue
        if k == "xml_id":
            attrib[f"{{{XML_NS}}}id"] = v
        else:
            attrib[k] = v
    el = ET.SubElement(parent, f"{{{TEI_NS}}}{tag}", attrib=attrib)
    if text is not None:
        el.text = text
    return el


def pos_to_teigr(pos: str) -> str:
    mapping = {
        "noun": "n",
        "verb": "v",
        "adjective": "adj",
        "adverb": "adv",
        "interjection": "int",
        "particle": "part",
        "pronoun": "pron",
        "determiner": "det",
        "preposition": "prep",
        "conjunction": "conj",
        "phrase": "phrase",
        "other": "other",
    }
    return mapping.get(pos, pos)


def entry_to_tei(parent: ET.Element, entry: dict) -> None:
    eid = entry["id"]
    ent = _sub(parent, "entry", type="main", xml_id=eid)

    form = _sub(ent, "form", type="lemma")
    _sub(form, "orth", entry["standard_spelling"])

    gram = _sub(ent, "gramGrp")
    _sub(gram, "pos", pos_to_teigr(entry["part_of_speech"]))

    for i, definition in enumerate(entry.get("definitions", []), 1):
        sense = _sub(ent, "sense", xml_id=f"{eid}.{i}")
        _sub(sense, "def", definition)
        for ex in entry.get("example_sentences", []):
            cit = _sub(sense, "cit", type="example")
            _sub(cit, "quote", ex)

    for variant in entry.get("informal_variants", []):
        vform = _sub(ent, "form", type="variant")
        _sub(vform, "orth", variant)

    if entry.get("pronunciation"):
        pron = _sub(ent, "form", type="pronunciation")
        _sub(pron, "orth", entry["pronunciation"])

    if entry.get("notes"):
        note = _sub(ent, "note")
        note.text = entry["notes"]


def build_tei(entries: list[dict]) -> ET.ElementTree:
    tei = ET.Element(f"{{{TEI_NS}}}TEI", attrib={"version": "5.0"})
    header = _sub(tei, "teiHeader")
    file_desc = _sub(header, "fileDesc")
    title_stmt = _sub(file_desc, "titleStmt")
    _sub(title_stmt, "title", "Naijá Live Dictionary — IFRA/NLA Standard Naijá Orthography")
    pub = _sub(file_desc, "publicationStmt")
    _sub(pub, "p", f"Generated {date.today().isoformat()}. Canonical source: data/dictionary.json.")
    src = _sub(file_desc, "sourceDesc")
    _sub(src, "p", "IFRA/NLA Guide to Standard Naijá Orthography (2010). See docs/citation-pack.md.")

    text = _sub(tei, "text")
    body = _sub(text, "body")
    for entry in entries:
        entry_to_tei(body, entry)
    return ET.ElementTree(tei)


def export_tei(dict_path: Path = DICT_PATH, out_path: Path = DEFAULT_OUT) -> int:
    entries = json.loads(dict_path.read_text(encoding="utf-8"))
    tree = build_tei(entries)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(out_path, encoding="utf-8", xml_declaration=True)
    print(f"Exported {len(entries)} entries -> {out_path}")
    return len(entries)


def main(argv: list[str]) -> int:
    out = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUT
    try:
        export_tei(out_path=out)
    except Exception as exc:
        print(f"export failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
