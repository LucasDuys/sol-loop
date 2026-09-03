# External results

Sol-loop vs muse-only on the same slices, plus dated leaderboard quotes in PUBLISHED.md.

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
### smoke-1-solonly (sol-only, backend codex)

pass 1/6

| task | pass | spec shape | planner s | sol units | check detail |
|---|---|---|---|---|---|
| py1-slugify | pass | n/a | 29.3 | 12.208 | py1 OK |
| py2-deep-merge | fail | n/a | 11.5 | 9.054 |   File "/Users/lucasduys/dev/sol-loop/evals/external/runs/smoke-1-solonly/py2-deep-merge/work/merge.py", line 2, in deep_merge |     raise NotImplementedError | NotImplementedError |
| py3-batches | fail | n/a | 3.5 | n/a |   File "/Users/lucasduys/dev/sol-loop/evals/external/runs/smoke-1-solonly/py3-batches/work/batches.py", line 2, in batches |     raise NotImplementedError | NotImplementedError |
| ts1-slugify | fail | n/a | 3.4 | n/a |     at async asyncRunEntryPointWithESMLoader (node:internal/modules/run_main:101:5) |  | Node.js v24.18.0 |
| ts2-unique | fail | n/a | 3.6 | n/a |     at async asyncRunEntryPointWithESMLoader (node:internal/modules/run_main:101:5) |  | Node.js v24.18.0 |
| ts3-memoize | fail | n/a | 3.3 | n/a |     at async asyncRunEntryPointWithESMLoader (node:internal/modules/run_main:101:5) |  | Node.js v24.18.0 |
## Comparison 2026-09-03

| run (harness) | accuracy | avg Sol wall s | avg Sol units | throughput, tasks per hour |
|---|---|---|---|---|
| smoke-1 (sol-loop) | 6/6 | 10.4 | 9.07 | 346.2 |
| smoke-1-baseline (muse-only) | 6/6 | 0.0 | n/a | n/a |
| smoke-1-solonly (sol-only) | 1/1 (5 invalid: rate limited) | 29.3 | 12.21 | 122.9 |

Wall time covers the Sol side only. Executor time is recorded by hand in this environment. Sol units ride the 20 EUR subscription at 0 EUR marginal, so the saving vs Sol-only is rate limit and latency, not euros. Euro savings apply against metered API models, see PUBLISHED.md.

## SWE-bench Verified starter slice 2026-09-03

Four real instances, two repos, both arms executed by hand from first principles (no upstream patch peeking). Official Docker grading where the hub serves this machine.

| Instance | sol-loop arm | muse-only baseline | Patches |
|---|---|---|---|
| psf__requests-1921 (session headers None) | resolved, official | resolved, official | identical |
| psf__requests-2317 (bytes method) | resolved, official | resolved, official | identical |
| pytest-dev__pytest-7490 (dynamic xfail) | fix verified by local fail to pass repro A/B | same patch | identical |
| pytest-dev__pytest-7571 (caplog level leak) | fix verified by local fail to pass repro A/B | same patch | identical |

Official reports: `runs/official-reports/swe-4-sol-loop.json` and `swe-4-baseline.json`. Sol planner cost held at 9 to 13 units per SPEC. The pytest pair cannot grade officially on Apple Silicon: the hub has no arm64 instance images for them and x86_64 pulls resolve arm64 under this daemon (documented in the run logs). Their fixes were verified instead by running the issue repros with and without the patch: xfailed vs failed, 2 passed vs leak. Same patches both arms, so one verification covers both.

Reading: on tasks the executor can solve, both arms converge to the same patch. The loop's value here is process, not a different answer: pinned SPEC, allow list scope, evidence trail, and planning at ~9 units flat instead of ~12 plus units implementing directly. The accuracy gap, if any, shows on tasks the executor cannot solve unaided. That is the next slice.
