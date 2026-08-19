# Citation Pack — Naijá Live Dictionary

**Purpose:** Academic attribution for the Live Dictionary, corpora, and orthography authorities (Phase 5b).

---

## Project (this repository)

```bibtex
@misc{naija-live-dictionary-2026,
  title        = {Naijá Live Dictionary: IFRA/NLA Standard Naijá Orthography Reference},
  year         = {2026},
  note         = {Structured dictionary with informal variant mapping. data/dictionary.json canonical; TEI export via export/tei_lex0.py}
}
```

---

## Orthography authority

```bibtex
@book{ofulue-esizimetor-2010-sno,
  title     = {Guide to Standard Naijá Orthography: An NLA Harmonized Writing System for Common Naijá Publications},
  author    = {Ofulue, Christine and Esizimetor, E.},
  year      = {2010},
  publisher = {IFRA Nigeria / NLA},
  note      = {Primary authority for standard_spelling (Decision D1). Do not republish full guide text without IFRA permission (D4).}
}
```

---

## Corpora used in variant pipeline

### NaijaSenti

```bibtex
@inproceedings{muhammad2022naijasenti,
  title     = {NaijaSenti: A Nigerian Twitter Sentiment Corpus for Multilingual Sentiment Analysis},
  author    = {Muhammad, Shamsuddeen Hassan and Adelani, David Ifeoluwa and others},
  booktitle = {LREC},
  year      = {2022},
  url       = {https://aclanthology.org/2022.lrec-1.63/}
}
```

### CENCOS

```bibtex
@misc{agbo-plag-2022-cencos,
  title        = {CENCOS: Corpus of English-Nigerian Pidgin Code-Switching},
  author       = {Agbo, Monday and Plag, Ingo},
  year         = {2022},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.7314016},
  url          = {https://zenodo.org/records/7314016}
}
```

### UD Naija-NSC (if used for examples)

```bibtex
@misc{caron2020naija,
  title  = {Naija Treebank (UD\_Naija-NSC)},
  author = {Caron, Bernard and others},
  year   = {2020},
  note   = {CC BY-SA 4.0. https://github.com/UniversalDependencies/UD_Naija-NSC}
}
```

### Mozilla Common Voice pcm (if used for pronunciation)

```bibtex
@misc{commonvoice-pcm,
  title  = {Common Voice — Nigerian Pidgin (pcm) subset},
  author = {{Mozilla Foundation}},
  note   = {CC0. https://commonvoice.mozilla.org/}
}
```

---

## NLP / methods references

### Orthographic variation (variant suggester)

```bibtex
@inproceedings{lin2024pcm-variation,
  title     = {Modeling Orthographic Variation Improves NLP Performance for Nigerian Pidgin},
  author    = {Lin, Yuxin and others},
  booktitle = {LREC-COLING},
  year      = {2024},
  url       = {https://aclanthology.org/2024.lrec-main.1006/}
}
```

### Sociolinguistic standardization context

```bibtex
@article{deuber-hinrichs-2007,
  title   = {Dynamics of Orthographic Standardization in Jamaican Creole and Nigerian Pidgin},
  author  = {Deuber, Dagmar and Hinrichs, Lars},
  journal = {English World-Wide},
  year    = {2007},
  doi     = {10.1111/j.1467-971X.2007.00486.x}
}
```

---

## TEI Lex-0 export

When citing the exported lexicon file:

> Naijá Live Dictionary (2026). TEI Lex-0 export `export/naija-dictionary.lex0.xml`. Canonical JSON: `data/dictionary.json`. Orthography: IFRA/NLA SNO.

TEI Lex-0 standard: https://lex-0.org/

---

## License notes (Decision D4)

| Asset | Status |
|-------|--------|
| `data/dictionary.json` (definitions/examples) | Project-authored seed; check IFRA before public republication of SNO-derived content |
| IFRA SNO guide | **D4 RESOLVED** — cite; do not republish full text without permission (`docs/d4-public-release-licensing.md`) |
| NaijaSenti / CENCOS | Academic use with citation; see dataset licenses |
| TEI export | Same as underlying dictionary; attribute this project |
