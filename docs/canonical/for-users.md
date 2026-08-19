# For users

Simple guide derived from the project manuscript. Full scientific detail: [`../manuscripts/naija-live-dictionary.md`](../manuscripts/naija-live-dictionary.md).

## What you can do

Open the Live Dictionary in a browser (after starting the local server) and:

1. Search a **standard** Naijá spelling (IFRA/NLA style).
2. Search an **informal** spelling (e.g. `pickin`, `book`, `dey`).
3. See the **standard form**, meaning, examples, and pronunciation hint.

If your spelling is close but not exact, the site may suggest a nearby match (“Did you mean?”).

## How to run it

From the project folder:

```bash
python web/serve.py
```

Then open: http://localhost:8765/web/

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

Start at `/web/docs/`.
