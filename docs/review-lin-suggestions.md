# Lin Suggestion Review (Batch 2)

Sorted by corpus count (desc). Use this for manual approve/reject before adding to `variant_mappings.json`.

**Auto batch 2 rule:** `method=lin`, count ≥ 5, forward Lin match, not blocklisted, not already mapped.

| Count | Variant | → SNO | entry_id | Fwd | Auto? | Notes |
|------:|---------|-------|----------|:---:|-------|-------|
| 521 | `she` | che | `che` | yes | N | english blocklist, known false positive |
| 503 | `they` | dei | `dei` | no | N | english blocklist, known false positive, not forward lin match |
| 140 | `They` | dei | `dei` | no | N | english blocklist, known false positive, not forward lin match |
| 123 | `She` | che | `che` | yes | N | english blocklist, known false positive |
| 52 | `try` | tri | `tri` | yes | N | english blocklist, known false positive |
| 40 | `done` | don | `don` | no | N | english blocklist, known false positive, not forward lin match |
| 33 | `than` | dan | `dan` | no | N | english blocklist, known false positive, not forward lin match |
| 32 | `reach` | rich | `rich` | no | N | english blocklist, known false positive, not forward lin match |
| 30 | `check` | shek | `shek` | no | N | english blocklist, known false positive, not forward lin match |
| 26 | `three` | tri | `tri` | no | N | english blocklist, known false positive, not forward lin match |
| 21 | `State` | stat | `stat` | no | N | english blocklist, known false positive, not forward lin match |
| 10 | `both` | bot | `bot` | no | N | english blocklist, known false positive, not forward lin match |
| 10 | `date` | dat | `dat` | no | N | english blocklist, known false positive, not forward lin match |
| 9 | `cash` | kach | `kach` | yes | N | already mapped |
| 6 | `bath` | bad | `bad` | no | N | english blocklist, known false positive, not forward lin match |
| 5 | `Try` | tri | `tri` | yes | N | english blocklist, known false positive |
| 5 | `state` | stat | `stat` | no | N | english blocklist, known false positive, not forward lin match |
| 4 | `com` | kom | `kom` | yes | N | already mapped, count < 5 |
| 3 | `Check` | shek | `shek` | no | N | english blocklist, known false positive, not forward lin match, count < 5 |
| 3 | `Three` | tri | `tri` | no | N | english blocklist, known false positive, not forward lin match, count < 5 |
| 3 | `ride` | rid | `rid` | no | N | not forward lin match, count < 5 |
| 3 | `steal` | stil | `stil` | no | N | not forward lin match, count < 5 |
| 2 | `Both` | bot | `bot` | no | N | english blocklist, known false positive, not forward lin match, count < 5 |
| 2 | `lege` | leg | `leg` | no | N | not forward lin match, count < 5 |
| 2 | `luck` | luk | `luk` | no | N | not forward lin match, count < 5 |
| 2 | `peak` | pik | `pik` | no | N | not forward lin match, count < 5 |
| 2 | `sweat` | swit | `swit` | no | N | not forward lin match, count < 5 |
| 1 | `Bright` | brit | `brit` | no | N | not forward lin match, count < 5 |
| 1 | `DY` | di | `di` | yes | N | count < 5 |
| 1 | `Mac` | make | `make` | yes | N | count < 5 |
| 1 | `Sweat` | swit | `swit` | no | N | not forward lin match, count < 5 |
| 1 | `bell` | belle | `belle` | yes | N | count < 5 |
| 1 | `deme` | dem | `dem` | no | N | not forward lin match, count < 5 |
| 1 | `dise` | dis | `dis` | no | N | not forward lin match, count < 5 |
| 1 | `een` | in | `in` | no | N | not forward lin match, count < 5 |
| 1 | `peace` | pik | `pik` | no | N | not forward lin match, count < 5 |
| 1 | `pic` | pik | `pik` | yes | N | count < 5 |
| 1 | `woke` | wok | `wok` | no | N | not forward lin match, count < 5 |

**Total lin suggestions:** 38 · **Auto-approved by batch 2 rule:** 0

## Manual review candidates (count ≥ 2, not auto)

These failed auto rules but may still be valid — review individually:

- `she` → **che** (che), count=521 — english blocklist, known false positive
- `they` → **dei** (dei), count=503 — english blocklist, known false positive, not forward lin match
- `They` → **dei** (dei), count=140 — english blocklist, known false positive, not forward lin match
- `She` → **che** (che), count=123 — english blocklist, known false positive
- `try` → **tri** (tri), count=52 — english blocklist, known false positive
- `done` → **don** (don), count=40 — english blocklist, known false positive, not forward lin match
- `than` → **dan** (dan), count=33 — english blocklist, known false positive, not forward lin match
- `reach` → **rich** (rich), count=32 — english blocklist, known false positive, not forward lin match
- `check` → **shek** (shek), count=30 — english blocklist, known false positive, not forward lin match
- `three` → **tri** (tri), count=26 — english blocklist, known false positive, not forward lin match
- `State` → **stat** (stat), count=21 — english blocklist, known false positive, not forward lin match
- `both` → **bot** (bot), count=10 — english blocklist, known false positive, not forward lin match
- `date` → **dat** (dat), count=10 — english blocklist, known false positive, not forward lin match
- `cash` → **kach** (kach), count=9 — already mapped
- `bath` → **bad** (bad), count=6 — english blocklist, known false positive, not forward lin match
- `Try` → **tri** (tri), count=5 — english blocklist, known false positive
- `state` → **stat** (stat), count=5 — english blocklist, known false positive, not forward lin match
- `com` → **kom** (kom), count=4 — already mapped, count < 5
- `Check` → **shek** (shek), count=3 — english blocklist, known false positive, not forward lin match, count < 5
- `Three` → **tri** (tri), count=3 — english blocklist, known false positive, not forward lin match, count < 5
- `ride` → **rid** (rid), count=3 — not forward lin match, count < 5
- `steal` → **stil** (stil), count=3 — not forward lin match, count < 5
- `Both` → **bot** (bot), count=2 — english blocklist, known false positive, not forward lin match, count < 5
- `lege` → **leg** (leg), count=2 — not forward lin match, count < 5
- `luck` → **luk** (luk), count=2 — not forward lin match, count < 5
- `peak` → **pik** (pik), count=2 — not forward lin match, count < 5
- `sweat` → **swit** (swit), count=2 — not forward lin match, count < 5
