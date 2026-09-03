# External results

Sol-loop vs muse-only on the same slices, plus dated leaderboard quotes in PUBLISHED.md.

### smoke-1 (sol-loop, backend codex)

pass 3/6

| task | pass | spec shape | planner s | sol units | check detail |
|---|---|---|---|---|---|
| py1-slugify | pass | pass | 9.9 | 9.001 | py1 OK |
| py2-deep-merge | pass | pass | 12.4 | 9.184 | py2 OK |
| py3-batches | pass | pass | 7.6 | 8.942 | py3 OK |
| ts1-slugify | fail | pass | 9.9 | 9.032 |     at async node:internal/modules/esm/loader:224:26 |  | Node.js v24.18.0 |
| ts2-unique | fail | pass | 9.8 | 9.060 |     at async node:internal/modules/esm/loader:224:26 |  | Node.js v24.18.0 |
| ts3-memoize | fail | pass | 12.8 | 9.226 |     at async node:internal/modules/esm/loader:224:26 |  | Node.js v24.18.0 |

### smoke-1-baseline (muse-only, backend mock)

pass 3/6

| task | pass | spec shape | planner s | sol units | check detail |
|---|---|---|---|---|---|
| py1-slugify | pass | n/a | 0 | n/a | py1 OK |
| py2-deep-merge | pass | n/a | 0 | n/a | py2 OK |
| py3-batches | pass | n/a | 0 | n/a | py3 OK |
| ts1-slugify | fail | n/a | 0 | n/a |     at async node:internal/modules/esm/loader:224:26 |  | Node.js v24.18.0 |
| ts2-unique | fail | n/a | 0 | n/a |     at async node:internal/modules/esm/loader:224:26 |  | Node.js v24.18.0 |
| ts3-memoize | fail | n/a | 0 | n/a |     at async node:internal/modules/esm/loader:224:26 |  | Node.js v24.18.0 |

### smoke-1 (sol-loop, backend codex)

pass 3/6

| task | pass | spec shape | planner s | sol units | check detail |
|---|---|---|---|---|---|
| py1-slugify | pass | pass | 9.9 | 9.001 | py1 OK |
| py2-deep-merge | pass | pass | 12.4 | 9.184 | py2 OK |
| py3-batches | pass | pass | 7.6 | 8.942 | py3 OK |
| ts1-slugify | fail | pass | 9.9 | 9.032 |     at node:internal/main/run_main_module:33:47 |  | Node.js v24.18.0 |
| ts2-unique | fail | pass | 9.8 | 9.060 |     at node:internal/main/run_main_module:33:47 |  | Node.js v24.18.0 |
| ts3-memoize | fail | pass | 12.8 | 9.226 |     at node:internal/main/run_main_module:33:47 |  | Node.js v24.18.0 |

### smoke-1-baseline (muse-only, backend mock)

pass 3/6

| task | pass | spec shape | planner s | sol units | check detail |
|---|---|---|---|---|---|
| py1-slugify | pass | n/a | 0 | n/a | py1 OK |
| py2-deep-merge | pass | n/a | 0 | n/a | py2 OK |
| py3-batches | pass | n/a | 0 | n/a | py3 OK |
| ts1-slugify | fail | n/a | 0 | n/a |     at node:internal/main/run_main_module:33:47 |  | Node.js v24.18.0 |
| ts2-unique | fail | n/a | 0 | n/a |     at node:internal/main/run_main_module:33:47 |  | Node.js v24.18.0 |
| ts3-memoize | fail | n/a | 0 | n/a |     at node:internal/main/run_main_module:33:47 |  | Node.js v24.18.0 |

### smoke-1 (sol-loop, backend codex)

pass 6/6

| task | pass | spec shape | planner s | sol units | check detail |
|---|---|---|---|---|---|
| py1-slugify | pass | pass | 9.9 | 9.001 | py1 OK |
| py2-deep-merge | pass | pass | 12.4 | 9.184 | py2 OK |
| py3-batches | pass | pass | 7.6 | 8.942 | py3 OK |
| ts1-slugify | pass | pass | 9.9 | 9.032 | ts1 OK |
| ts2-unique | pass | pass | 9.8 | 9.060 | ts2 OK |
| ts3-memoize | pass | pass | 12.8 | 9.226 | ts3 OK |

### smoke-1-baseline (muse-only, backend mock)

pass 6/6

| task | pass | spec shape | planner s | sol units | check detail |
|---|---|---|---|---|---|
| py1-slugify | pass | n/a | 0 | n/a | py1 OK |
| py2-deep-merge | pass | n/a | 0 | n/a | py2 OK |
| py3-batches | pass | n/a | 0 | n/a | py3 OK |
| ts1-slugify | pass | n/a | 0 | n/a | ts1 OK |
| ts2-unique | pass | n/a | 0 | n/a | ts2 OK |
| ts3-memoize | pass | n/a | 0 | n/a | ts3 OK |

