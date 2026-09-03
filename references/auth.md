# Auth

Live mode needs your GPT account once. Until then everything runs in mock mode.

## Mock mode (works now, no auth)

```bash
SOL_BACKEND=mock scripts/run.sh --goal GOAL.md --allow allow.txt
python3 scripts/bench.py --backend mock
```

Mock planner emits a SPEC from the case file template. Executor still runs for real on Muse. Benchmarks in this mode measure executor quality and harness enforcement, not Sol quality.

## Live mode (after you auth)

1. Sign in Codex CLI once on this Mac:
```bash
codex auth login
codex exec --skip-git-repo-check -s read-only -C "$HOME" "reply with exactly OK"
```
2. Run the loop (uses the model in `~/.codex/config.toml`, here `gpt-5.6-sol` at `xhigh` reasoning effort; override with `SOL_MODEL=...`):
```bash
SOL_BACKEND=codex scripts/run.sh --goal GOAL.md --allow allow.txt
```
3. Re run benchmarks and compare mock vs live in `evals/BENCHMARKS.md`.

## Rules

- Secrets never travel through prompts or chat. Tokens live in env vars. Never hardcode.
- Send Sol only goal plus evidence plus allow list. Never dump the repo into Sol.
- Keep `approval-policy: never` with `sandbox: read-only` for planning turns. Executor writes only inside the working directory.
- Auth state is machine state, not a fact to hard code. Probe it per run. If the probe fails, report BLOCKED and stay in mock mode.
