# Naijá SNO — Keyman keyboard (II-5b)

System-wide typing for IFRA/NLA Standard Naijá Orthography digraphs and high-tone acute vowels. Consumes the II-5a lexicon export; does **not** write `data/dictionary.json`.

## Digraph / acute behavior

| Sequence | Output |
|----------|--------|
| `g` then `b` | `gb` |
| `k` then `p` | `kp` |
| `s` then `h` | `sh` |
| `c` then `h` | `ch` |
| `z` then `h` | `zh` |
| `'` then `a`/`e`/`i`/`o`/`u` | `á`/`é`/`í`/`ó`/`ú` |

Other Latin letters pass through. No whole-English-word auto-replace in the keyboard; suggestions come from the wordlist / lexical model.

## Files

| File | Role |
|------|------|
| `naija_sno.kmn` | Keyboard rules (digraph + acute) |
| `naija_sno.kps` | Package metadata |
| `naija_sno.wordlist.tsv` | Generated wordlist (`word` + `count`) |
| `readme.txt` | Short package readme for Keyman install |

## Regenerate wordlist

After growing the Live Dictionary and refreshing the IME export:

```bash
python data/export_ime_lexicon.py
python data/export_keyman_wordlist.py
```

Self-check (digraphs in `.kmn`, non-empty wordlist):

```bash
python data/export_keyman_wordlist.py --self-check
```

## Build and install (local)

Requires Node.js 20+ (for `npx @keymanapp/kmc`). Keyman Developer GUI is optional.

```bash
cd ime/keyman/naija_sno
npx --yes @keymanapp/kmc@18 build naija_sno.kmn -o build/naija_sno.kmx
npx --yes @keymanapp/kmc@18 build naija_sno.kps -o build/naija_sno.kmp
```

Then install [Keyman](https://keyman.com/), open `build/naija_sno.kmp`, enable **Naijá SNO**.

Prebuilt `.kmp` binaries are not committed (`build/` is gitignored).

## Related

- Spec: `docs/superpowers/specs/2026-09-27-part-ii-5b-keyman-design.md`
- Phase note: `docs/phase-ii-5b-keyman.md`
- Lexicon export: `data/ime/`
