# Lin Suggestion Review (Batch 2)

Sorted by corpus count (desc). Use this for manual approve/reject before adding to `variant_mappings.json`.

**Auto batch 2 rule:** `method=lin`, count ≥ 5, forward Lin match, not blocklisted, not already mapped.

| Count | Variant | → SNO | entry_id | Fwd | Auto? | Notes |
|------:|---------|-------|----------|:---:|-------|-------|
| 1701 | `she` | che | `che` | yes | N | english blocklist, known false positive |
| 1560 | `they` | dei | `dei` | no | N | english blocklist, known false positive, not forward lin match |
| 727 | `try` | tri | `tri` | yes | N | english blocklist, known false positive |
| 695 | `reach` | rich | `rich` | no | N | english blocklist, known false positive, not forward lin match |
| 592 | `three` | tri | `tri` | no | N | english blocklist, known false positive, not forward lin match |
| 447 | `They` | dei | `dei` | no | N | english blocklist, known false positive, not forward lin match |
| 299 | `She` | che | `che` | yes | N | english blocklist, known false positive |
| 223 | `check` | shek | `shek` | no | N | english blocklist, known false positive, not forward lin match |
| 206 | `State` | stat | `stat` | no | N | english blocklist, known false positive, not forward lin match |
| 157 | `state` | stat | `stat` | no | N | english blocklist, known false positive, not forward lin match |
| 138 | `done` | don | `don` | no | N | english blocklist, known false positive, not forward lin match |
| 114 | `than` | dan | `dan` | no | N | english blocklist, known false positive, not forward lin match |
| 98 | `peace` | pik | `pik` | no | N | not forward lin match |
| 75 | `date` | dat | `dat` | no | N | english blocklist, known false positive, not forward lin match |
| 61 | `fry` | fri | `fri` | yes | N | english blocklist, known false positive |
| 58 | `white` | wit | `wit` | no | N | not forward lin match |
| 48 | `steal` | stil | `stil` | no | N | not forward lin match |
| 40 | `bath` | bad | `bad` | no | N | english blocklist, known false positive, not forward lin match |
| 39 | `both` | bot | `bot` | no | N | english blocklist, known false positive, not forward lin match |
| 32 | `style` | stil | `stil` | no | N | not forward lin match |
| 24 | `sele` | sel | `sel` | no | N | not forward lin match |
| 21 | `ride` | rid | `rid` | no | N | not forward lin match |
| 16 | `Peace` | pik | `pik` | no | N | not forward lin match |
| 12 | `Wike` | wik | `wik` | no | N | not forward lin match |
| 12 | `luck` | luk | `luk` | no | N | not forward lin match |
| 11 | `hole` | hol | `hol` | no | N | not forward lin match |
| 9 | `Both` | bot | `bot` | no | N | english blocklist, known false positive, not forward lin match |
| 9 | `Check` | shek | `shek` | no | N | english blocklist, known false positive, not forward lin match |
| 9 | `woke` | wok | `wok` | no | N | not forward lin match |
| 8 | `Try` | tri | `tri` | yes | N | english blocklist, known false positive |
| 7 | `bright` | brit | `brit` | no | N | not forward lin match |
| 7 | `sweat` | swit | `swit` | no | N | not forward lin match |
| 6 | `Luke` | luk | `luk` | no | N | not forward lin match |
| 6 | `Theo` | di | `di` | no | N | not forward lin match |
| 5 | `bore` | bor | `bor` | no | N | not forward lin match |
| 4 | `Ea` | I | `i` | no | N | not forward lin match, count < 5 |
| 4 | `Three` | tri | `tri` | no | N | english blocklist, known false positive, not forward lin match, count < 5 |
| 4 | `buck` | buk | `buk` | no | N | not forward lin match, count < 5 |
| 4 | `feet` | fit | `fit` | no | N | not forward lin match, count < 5 |
| 4 | `pol` | ple | `ple` | yes | N | count < 5 |
| 4 | `pu` | poo | `poo` | yes | N | count < 5 |
| 4 | `sy` | si | `si` | yes | N | count < 5 |
| 3 | `thee` | di | `di` | no | N | not forward lin match, count < 5 |
| 2 | `Beacause` | bikos | `bikos` | no | N | not forward lin match, count < 5 |
| 2 | `lege` | leg | `leg` | no | N | not forward lin match, count < 5 |
| 2 | `peak` | pik | `pik` | no | N | not forward lin match, count < 5 |
| 2 | `spy` | spie | `spie` | yes | N | count < 5 |
| 1 | `Bright` | brit | `brit` | no | N | not forward lin match, count < 5 |
| 1 | `DY` | di | `di` | yes | N | count < 5 |
| 1 | `Mac` | make | `make` | yes | N | count < 5 |
| 1 | `Reach` | rich | `rich` | no | N | english blocklist, not forward lin match, count < 5 |
| 1 | `Sweat` | swit | `swit` | no | N | not forward lin match, count < 5 |
| 1 | `bell` | belle | `belle` | yes | N | count < 5 |
| 1 | `ea` | I | `i` | no | N | not forward lin match, count < 5 |
| 1 | `een` | in | `in` | no | N | not forward lin match, count < 5 |
| 1 | `thi` | di | `di` | no | N | not forward lin match, count < 5 |
| 1 | `vain` | fain | `find` | yes | N | count < 5 |

**Total lin suggestions:** 57 · **Auto-approved by batch 2 rule:** 0

## Manual review candidates (count ≥ 2, not auto)

These failed auto rules but may still be valid — review individually:

- `she` → **che** (che), count=1701 — english blocklist, known false positive
- `they` → **dei** (dei), count=1560 — english blocklist, known false positive, not forward lin match
- `try` → **tri** (tri), count=727 — english blocklist, known false positive
- `reach` → **rich** (rich), count=695 — english blocklist, known false positive, not forward lin match
- `three` → **tri** (tri), count=592 — english blocklist, known false positive, not forward lin match
- `They` → **dei** (dei), count=447 — english blocklist, known false positive, not forward lin match
- `She` → **che** (che), count=299 — english blocklist, known false positive
- `check` → **shek** (shek), count=223 — english blocklist, known false positive, not forward lin match
- `State` → **stat** (stat), count=206 — english blocklist, known false positive, not forward lin match
- `state` → **stat** (stat), count=157 — english blocklist, known false positive, not forward lin match
- `done` → **don** (don), count=138 — english blocklist, known false positive, not forward lin match
- `than` → **dan** (dan), count=114 — english blocklist, known false positive, not forward lin match
- `peace` → **pik** (pik), count=98 — not forward lin match
- `date` → **dat** (dat), count=75 — english blocklist, known false positive, not forward lin match
- `fry` → **fri** (fri), count=61 — english blocklist, known false positive
- `white` → **wit** (wit), count=58 — not forward lin match
- `steal` → **stil** (stil), count=48 — not forward lin match
- `bath` → **bad** (bad), count=40 — english blocklist, known false positive, not forward lin match
- `both` → **bot** (bot), count=39 — english blocklist, known false positive, not forward lin match
- `style` → **stil** (stil), count=32 — not forward lin match
- `sele` → **sel** (sel), count=24 — not forward lin match
- `ride` → **rid** (rid), count=21 — not forward lin match
- `Peace` → **pik** (pik), count=16 — not forward lin match
- `Wike` → **wik** (wik), count=12 — not forward lin match
- `luck` → **luk** (luk), count=12 — not forward lin match
- `hole` → **hol** (hol), count=11 — not forward lin match
- `Both` → **bot** (bot), count=9 — english blocklist, known false positive, not forward lin match
- `Check` → **shek** (shek), count=9 — english blocklist, known false positive, not forward lin match
- `woke` → **wok** (wok), count=9 — not forward lin match
- `Try` → **tri** (tri), count=8 — english blocklist, known false positive
- `bright` → **brit** (brit), count=7 — not forward lin match
- `sweat` → **swit** (swit), count=7 — not forward lin match
- `Luke` → **luk** (luk), count=6 — not forward lin match
- `Theo` → **di** (di), count=6 — not forward lin match
- `bore` → **bor** (bor), count=5 — not forward lin match
- `Ea` → **I** (i), count=4 — not forward lin match, count < 5
- `Three` → **tri** (tri), count=4 — english blocklist, known false positive, not forward lin match, count < 5
- `buck` → **buk** (buk), count=4 — not forward lin match, count < 5
- `feet` → **fit** (fit), count=4 — not forward lin match, count < 5
- `pol` → **ple** (ple), count=4 — count < 5
- `pu` → **poo** (poo), count=4 — count < 5
- `sy` → **si** (si), count=4 — count < 5
- `thee` → **di** (di), count=3 — not forward lin match, count < 5
- `Beacause` → **bikos** (bikos), count=2 — not forward lin match, count < 5
- `lege` → **leg** (leg), count=2 — not forward lin match, count < 5
- `peak` → **pik** (pik), count=2 — not forward lin match, count < 5
- `spy` → **spie** (spie), count=2 — count < 5
