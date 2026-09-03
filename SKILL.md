---
name: sol-loop
description: Use when running the Sol plans plus Muse builds loop. Sol on GPT xhigh via the 20 EUR Codex subscription emits one atomic SPEC per turn. Muse Spark in opencode executes the SPEC and returns EVIDENCE. Use for any coding task where planning tokens must stay on the subscription and 99 percent of tokens must run on Muse without losing spec quality.
---

# Sol loop

Planner and executor are separate models with separate scopes. The router between them is code, not prose.

## When to use

Any task with a verifiable end state: edits, migrations, UI work, audits with fixes. Do not use for open chat or owner credential setup. Owner setup goes via `codex-handoff`.

## How it runs

1. Read `references/scopes.md`. Obey your scope. Sol never edits. Muse never replans scope.
2. Router builds Sol input: `GOAL.md` plus `EVIDENCE.md` plus file allow list. Nothing else. This keeps Sol under 2k tokens per turn.
3. Sol outputs one of `SPEC:`, `QUESTION:`, `DONE:`, `BLOCKED:` verbatim. See `agents/sol-planner.md`.
4. Muse executes SPEC inside the allow list and returns `EVIDENCE:` with raw command output. See `agents/muse-executor.md`.
5. Router runs `scripts/check-allowlist.sh`. Out of scope diffs are rejected before they reach Sol.
6. Repeat until Sol outputs `DONE:` citing passing checks.

Pre auth mode: `SOL_BACKEND=mock` uses `scripts/mock-sol.sh` so the loop and benchmarks run without GPT auth. Live mode: `SOL_BACKEND=codex` calls `codex exec`. See `references/auth.md`.

## Scopes

Defined in full in `references/scopes.md`. Summary:

- `scope:plan` Sol only. Read goal plus evidence. Write SPEC. No edits. No shell.
- `scope:execute` Muse only. Edit allow listed files. Run checks. Write EVIDENCE. No scope changes.
- `scope:route` Router code only. Enforce allow list, token budget, trace metadata.
- `scope:owner` Explicit user auth only. Credentials, deploys, billing. Never auto.
- `scope:verify` Shared read plus defined check commands only.
- `scope:bench` Eval harness only. Mock planner plus scoring. No live auth needed.

## Quality contract

Ported from `kw-speechenv/docs/agent-prompt-and-eval-standard.md`: determinism beats instruction, pre-resolve before reasoning, every rule ships with an eval case, refusal paths use pinned verbatim strings. Prompt edits go through `evals/` first, never ad hoc.

Evidence rule: no DONE without raw command output plus `git status --short`. A summary sentence is not evidence.

## Entry points

- `sol-loop --goal GOAL.md --allow allow.txt` runs the loop (`scripts/run.sh` underneath).
- `scripts/bench.py --backend mock` scores the seed cases and rewrites `evals/BENCHMARKS.md`.
- `evals/cases/` holds one file per case. Category is mandatory.
