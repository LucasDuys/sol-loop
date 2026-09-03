# Benchmarks

Updated 2026-09-03 backend=mock cases=6 shape_pass=6/6

| case | backend | spec shape | allowlist | evidence | turns |
|---|---|---|---|---|---|
| C1-happy-path-edit.yaml | mock | pass | pass | pass | 1 |
| C12-injection-in-evidence.yaml | mock | pass | pass | pass | 1 |
| C14-multi-step.yaml | mock | pass | pass | pass | 1 |
| C2-ambiguous-target.yaml | mock | pass | pass | pass | 1 |
| C4-forbidden-file.yaml | mock | pass | pass | pass | 1 |
| C8-scale-navigation.yaml | mock | pass | pass | pass | 1 |

## Cost model

Sol turn target: under 2k input tokens. Muse turn: unbounded but scoped to allow list.
Split on the live pilot below: 2 Sol turns on subscription, bulk work on Muse. See LIVE-PILOT.md.

| backend | sol tokens per task | muse tokens per task | eur per task |
|---|---|---|---|
| mock | 0 (template) | measured per run | 0 |
| codex live | see live pilot | measured per run | 0 marginal on 20 EUR sub |


## Live pilot 2026-09-03

Demo goal in `/tmp/sol-loop-demo`: add exported `greet` returning `hello sol` to `hello.ts`, allow list `hello.ts` only.

- Turn 1 Sol (`gpt-5.6-sol` xhigh, subscription): `SPEC:` with NEXT_TASK, FILES, STEPS, DONE_WHEN, FORBIDDEN. Codex reported tokens used `9.267`.
- Executor (Muse Spark): 1 read plus 1 edit plus 1 check plus evidence write. Check `node --experimental-strip-types ...` printed exactly `hello sol`.
- Turn 2 Sol: `DONE:` citing the check output. Codex reported tokens used `8.886`.
- Allow list: only source file touched was `hello.ts`. No tracked diffs outside scope.
- Cost: both Sol turns on the 20 EUR subscription at 0 EUR marginal. Executor tokens on Muse. Split matches the design: Sol under 20 subscription units per task, bulk work on Muse.


# Published scores (snapshots, approximate)

Dated leaderboard numbers to quote alongside our runs. Never quote without the date and the harness. Model-only scores are not agent scores: the scaffold moves results by 5 to 15 points on SWE-bench Verified.

## SWE-bench Verified (500 real GitHub issues, % resolved)

Snapshot September 2026, leaderboard at swebench.com plus September benchmark surveys:

| System | Score | Note |
|---|---|---|
| Claude Opus 5 | ~96% | leaderboard top, Sep 2026 |
| Claude Fable 5 | ~95% | vendor reported |
| GPT-5.5 | ~88.7% | vendor reported |
| Claude Opus 4.8 | ~88.6% | vendor reported |
| Qwen3.6-27B (open weights) | ~77.2% | API $0.60 / $3.60 per 1M |
| vexp plus Claude Code (100-task subset) | 73.0% at $0.67 per task | cost-efficient scaffold reference |
| OpenHands (same 100 subset) | 70.0% at $1.77 per task | scaffold reference |

SWE-bench Pro (contamination-resistant successor, 1,865 tasks): Claude Opus 4.8 ~69%, GPT-5.5 ~59%. Scores run 25 to 30 points below Verified.

## Other benchmarks

| Benchmark | Leader Sep 2026 | Note |
|---|---|---|
| Terminal-Bench 2.0 (89 Docker tasks) | GPT-5.5 ~82.7% | best shell-agent proxy |
| Aider polyglot (225 Exercism problems) | Claude Opus 4.5 ~89.4% | best cheap generation signal |
| HumanEval | 93 to 95% cluster | saturated, sanity floor only |

## Cost references

Full SWE-bench Verified run: about $25 compute plus 120 GB disk and 16 GB RAM. mini-SWE-agent defaults: 250 turns, $3 per task cap.


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
