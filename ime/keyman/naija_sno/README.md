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

1. Install [Keyman](https://keyman.com/) for your OS, and optionally [Keyman Developer](https://keyman.com/developer/) to compile the package.
2. Open `naija_sno.kps` (or this folder) in Keyman Developer.
3. Build → produce `naija_sno.kmp`.
4. Install the `.kmp` in Keyman and enable **Naijá SNO**.

Prebuilt `.kmp` binaries are not committed; build locally. Keyman Developer is not required on CI or agent machines.

## Related

- Spec: `docs/superpowers/specs/2026-09-27-part-ii-5b-keyman-design.md`
- Phase note: `docs/phase-ii-5b-keyman.md`
- Lexicon export: `data/ime/`
