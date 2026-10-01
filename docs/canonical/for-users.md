# For users

Simple guide derived from the project manuscript. Full scientific detail: [`../manuscripts/naija-live-dictionary.md`](../manuscripts/naija-live-dictionary.md).

## What you can do

After starting the local server:

1. **Fix spelling** (primary): paste already-Pidgin text with messy spelling → SNO via the dictionary index.
2. **Dictionary search**: look up a standard or informal word; see meaning, examples, pronunciation hint.
3. **Advanced: English → Pidgin** (on the Fix spelling page): optional English sentence → Pidgin (local model) then SNO. Not for already-Pidgin cleanup.
4. **Keyman (Naija SNO):** type with digraphs/acutes in other apps (`ime/keyman/naija_sno/`).

If your spelling is close but not exact, the dictionary may show a “Did you mean?” **spelling suggestion** (not full autocorrect).

## How to run it

From the project folder:

```bash
python web/serve.py
```

Then open: http://localhost:8765/web/normalize.html (Fix spelling)  
Dictionary: http://localhost:8765/web/index.html

Do **not** double-click the HTML file alone — the dictionary data will not load.

## What “standard” means here

Spellings follow the **IFRA/NLA Standard Naijá Orthography** (2010). This project is **not** affiliated with IFRA Nigeria. Other common spellings are kept as *variants* that point to the standard form.

## More help on the website

| Layer | Topic |
|-------|--------|
| User Guide | How to search and read entries |
| IFRA Knowledge Center | Short orthography notes |
| Reproducibility | How builders verify the data |
| Tutorials | Step-by-step examples |

Growth policy (when the lexicon expands): [`../live-growth.md`](../live-growth.md).
