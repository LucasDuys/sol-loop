# External benchmarks

How sol-loop measures quality per cost and speed against public benchmarks.

## The shortlist

| Benchmark | What it measures | Size | Cost and time to run a slice | Needs | Relevance to sol-loop |
|---|---|---|---|---|---|
| Local smoke (this dir) | Mechanics check, executor sanity floor | 6 tasks, py plus ts | cents, minutes | nothing | Validates the adapter chain today |
| Aider polyglot style (Exercism) | Function from spec, 6 languages | 225 full, run 20 | cents, under an hour | Exercism track clones | Cheapest real executor signal |
| SWE-bench Verified 10-slice | Real GitHub issues, multi file patches | 500 full, run 10 | ~hours, Docker images | Docker, 120 GB free for full | Strongest engineering signal |
| LiveCodeBench (reference only) | Competitive programming generation | rolling | heavy scaffold | custom harness | Quoted from leaderboard, not run here |

HumanEval and MBPP are skipped as comparisons: saturated near ceiling since 2024 and contaminated. They work as a sanity floor only.

## Task format

One JSON object per line: `id`, `goal`, `allow` (list), `files` (starter path to content), `check` (shell command, exit 0 means pass).

```json
{"id": "py1-slugify", "goal": "Add ...", "allow": ["slug.py"], "files": {"slug.py": "...", "check_slug.py": "..."}, "check": "python3 check_slug.py"}
```

## Commands

Prepare a slice (planner step, timed, Sol units parsed from log):

```bash
python3 evals/external/run_slice.py --tasks evals/external/polyglot-smoke.jsonl --harness sol-loop --backend mock --out evals/external/runs/smoke-1/
python3 evals/external/run_slice.py --tasks evals/external/polyglot-smoke.jsonl --harness muse-only --out evals/external/runs/smoke-1-baseline/
```

`sol-loop` harness writes GOAL.md and runs the planner to SPEC. `muse-only` writes BRIEF.md with the raw goal and no SPEC. That pair is the baseline that isolates what the Sol SPEC step adds. Execute each task dir (SPEC or BRIEF), then grade:

```bash
python3 evals/external/run_slice.py --grade evals/external/runs/smoke-1/
python3 evals/external/run_slice.py --grade evals/external/runs/smoke-1-baseline/
```

Grading runs each task check and appends the comparison table to `evals/external/RESULTS.md`. Recorded per task: pass, planner wall seconds, Sol subscription units, executor notes (Muse tokens are recorded by hand in this environment).

## SWE-bench Verified 10-slice (heavy path)

```bash
pip install datasets swebench
python3 evals/external/run_slice.py --swe-ids evals/external/swe-10.txt --harness sol-loop --backend codex --out evals/external/runs/swe-10/
```

This fetches each instance from `princeton-nlp/SWE-bench_Verified`, clones the repo at the base commit, and writes GOAL.md from the problem statement. Allow list is `*` for this benchmark and that is recorded: scope enforcement is off, the official test suite is the judge. After execution, collect patches and grade with the official Docker harness:

```bash
python3 evals/external/run_slice.py --collect-patches evals/external/runs/swe-10/ > predictions.jsonl
python -m swebench.harness.run_evaluation --dataset_name princeton-nlp/SWE-bench_Verified --predictions_path predictions.jsonl --max_workers 4 --run_id sol-loop-1
```

Suggested starter set: 10 instances across at least 4 of the 12 repos. Full Verified needs 120 GB free disk and 16 GB RAM. A full run costs about $25 in compute per public cost reports.

## Reading results

`RESULTS.md` holds our runs. `PUBLISHED.md` holds dated leaderboard snapshots for the quote alongside. A claim quotes at least two together: our slice score plus the matching published number, with harness disclosed. Never quote the smoke set as a benchmark score. It is a mechanics check.
