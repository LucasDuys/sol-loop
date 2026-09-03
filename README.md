# sol-loop

Sol plans. Muse builds. You keep the 20 EUR subscription.

A two model loop: GPT xhigh on your Codex subscription emits one atomic SPEC per turn. Muse Spark in opencode does all the reading, editing, and testing, then returns EVIDENCE. Sol decides the next step. Over 99 percent of tokens run on Muse.

## Install

```bash
git clone https://github.com/LucasDuys/sol-loop.git && ./sol-loop/install.sh
```

Then use it in any repo:

```bash
cd your-repo
sol-loop --goal GOAL.md --allow allow.txt
```

No auth needed to start: mock mode works immediately, live mode lights up after `codex auth login`. The installer links the skill plus both agents into opencode and puts `sol-loop` on your PATH.

## Measured results

Three arms, same 6 py plus ts tasks, Sep 2026:

| Harness | Accuracy | Avg Sol cost per task | Avg Sol wall per task |
|---|---|---|---|
| sol-loop (Sol SPEC, Muse builds) | 6/6 | 9.1 units, 0 EUR marginal | 10.4s |
| muse-only (no planner) | 6/6 | 0 | 0 |
| sol-only (Sol builds directly) | 1/1 valid, 5 invalid | 12.2 units valid run | 29.3s valid run |

Two readings. On small tasks both Muse arms pass, so the slice proves mechanics and cost split, not a quality gap. And 5 of 6 sol-only runs died on the subscription usage limit while planner calls kept fitting: on a flat sub the scarce resource is rate limit, not euros, and planning cost stays flat while execution bulk rides Muse. Routing rules from the numbers: `references/routing.md`. Harder slices (20 task Exercism, 10 task SWE-bench Verified) are wired in `evals/external/`. For context, published Sep 2026 numbers run ~89 to 96% on SWE-bench Verified at the frontier and ~$0.67 to $1.77 per task for efficient scaffolds. Full tables in `evals/BENCHMARKS.md`.

## Why this exists

- Planning quality without API burn. Sol sees under 2k tokens per turn: goal plus evidence plus allow list. Never the repo.
- Executor quality without prompt bloat. Muse gets the full harness: allow list contract, skills on demand, MCP docs, browser verify.
- No silent scope creep. Router code rejects diffs outside the allow list before they reach Sol.
- No fake done. DONE requires raw command output plus git status. Summary prose does not count.

## Use in opencode

In any repo:

```bash
cd your-repo
echo "Your goal in one paragraph" > GOAL.md
printf 'src/area/file-a.ts\nsrc/area/file-b.ts\n' > allow.txt
sol-loop --goal GOAL.md --allow allow.txt
```

The router calls Sol for a SPEC, then tells you to run the executor step. In the opencode TUI that step is `@muse-executor` with the SPEC contents. It edits inside the allow list only, runs the check, and writes `EVIDENCE:`. Re run `run.sh` and Sol emits the next SPEC or `DONE:`.

Rules that keep it safe: Sol never sees your files, only goal plus evidence plus allow list. Diffs outside the allow list are rejected by `check-allowlist.sh` before they reach Sol. Nothing is DONE without raw command output.

## 30 second demo (no auth)

```bash
git clone https://github.com/LucasDuys/sol-loop.git && ./sol-loop/install.sh
echo "Fix checkout copy without touching layout" > GOAL.md
echo "src/checkout/copy.ts" > allow.txt
SOL_BACKEND=mock sol-loop --goal GOAL.md --allow allow.txt
python3 sol-loop/scripts/bench.py --backend mock
```

Live mode after you auth GPT once:

```bash
codex auth login
sol-loop --goal GOAL.md --allow allow.txt
```

## How it works

1. Sol outputs `SPEC:` with NEXT_TASK, FILES, STEPS, DONE_WHEN, FORBIDDEN. Or `QUESTION:`, `DONE:`, `BLOCKED:` verbatim.
2. Muse executes inside FILES only and returns `EVIDENCE:` with CHANGED, CHECKS, STATE, NEXT.
3. Router runs `check-allowlist.sh` and passes EVIDENCE back to Sol.

Full contracts in `SKILL.md` and `references/scopes.md`. Prompts in `agents/`. Ported from the Kenward agent prompt standard: determinism beats instruction, pre-resolve before reasoning, every rule ships with an eval case.

## Benchmarks

Seed suite in `evals/cases/`. Six cases across happy path, ambiguity, permission, scale, multi step, injection. Harness scores spec shape, allow list adherence, and evidence validity. Trajectory over prose.

See `evals/BENCHMARKS.md` for the latest table. Mock numbers run with no auth. A live pilot with measured subscription usage is in `evals/LIVE-PILOT.md`.

| case | what it proves |
|---|---|
| C1 happy path edit | Common case works in fewest calls |
| C2 ambiguous target | Asks one focused question instead of guessing |
| C4 forbidden file | BLOCKED with pinned string, zero out of scope writes |
| C8 scale navigation | Searches instead of loading the full tree |
| C14 multi step | Finishes dependent chain, asserts final state |
| C12 injection | Treats evidence payload as data, never follows it |

Run it:

```bash
python3 scripts/bench.py --backend mock
```

## Scopes

| scope | who | can | cannot |
|---|---|---|---|
| plan | Sol | read goal plus evidence, write SPEC | edit, shell, MCP, change goal |
| execute | Muse | edit allow listed files, run checks, write EVIDENCE | change scope, touch outside allow list |
| route | code | enforce allow list, budgets, traces | generate code, skip checks |
| owner | you | credentials, deploys, billing | never auto |
| verify | shared | defined check commands, headless browser | prod writes without flag |
| bench | harness | mock planner, scoring | needs no auth |

## Repo layout

```
install.sh             one command setup, links skill plus agents
SKILL.md               skill entry, load bearing order
agents/sol-planner.md  planner prompt, no tools
agents/muse-executor.md executor prompt, full tools
scripts/sol-loop       PATH entry point, calls run.sh
scripts/run.sh         router loop
scripts/mock-sol.sh    pre auth planner stand in
scripts/check-allowlist.sh L2 enforcement
scripts/bench.py       scoring plus BENCHMARKS.md writer
evals/cases/           one file per case, category mandatory
evals/BENCHMARKS.md    generated score table
evals/LIVE-PILOT.md    measured live run
references/scopes.md   scope definitions
references/routing.md  what to send sol-loop vs sol-only vs Fable
references/auth.md     mock now, codex live later
```

## Roadmap

- [x] Mock loop plus seed evals, no auth needed
- [x] Live codex backend pilot with measured usage
- [ ] Cost per task table across real tasks
- [ ] Nightly drift set from sampled traces

Built for opencode. Works with `codex-handoff` for owner credential steps.
