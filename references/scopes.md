# Scopes

One scope per role. Code enforces what prose states. If code can decide it, code decides it.

## scope:plan (Sol, GPT xhigh)

Can:
- Read `GOAL.md`, `EVIDENCE.md`, file allow list.
- Write one SPEC per turn in the shape in `agents/sol-planner.md`.
- Output `QUESTION:`, `DONE:`, `BLOCKED:` when the contract says so.

Cannot:
- Read repo files. Edit files. Run shell. Call MCP. Change the goal.
- Emit code or patches. Assign files outside the allow list.
- Output DONE without citing passing command output from EVIDENCE.

Token budget: under 2k input per turn. Goal plus evidence summary plus allow list only.

## scope:execute (Muse Spark, opencode subagent)

Can:
- Read SPEC plus repo state inside the working directory.
- Edit files listed in SPEC FILES.
- Run the check command in SPEC DONE_WHEN plus `git status --short` and `git diff --stat`.
- Load skills on demand: `impeccable`, `design-taste-frontend`, `astryx` for UI. `playwright` for browser verify. `context7` plus `gh_grep` for docs and examples.
- Write `EVIDENCE.md` in the shape in `agents/muse-executor.md`.

Cannot:
- Change goal or SPEC scope. Touch files outside SPEC FILES. Restyle adjacent code or live facing UI as a side effect.
- Run destructive commands (delete branch, publish, deploy, migrate prod) unless SPEC names them and the router flags `--allow-destructive`.
- Claim DONE. Only Sol outputs DONE.

## scope:route (router code in scripts/run.sh)

Can:
- Build Sol input. Pass SPEC to Muse. Run `check-allowlist.sh`. Attach trace metadata (`prompt_version`, `model_id`, `spec_id`, `case_category`).
- Reject out of scope diffs before they reach Sol. Count tokens per role per turn.

Cannot:
- Generate code. Edit SPEC text. Skip the allow list check.

## scope:owner (user auth only)

Any step needing logged in accounts, OAuth clients, API keys, DNS, billing, or account deletion. Not autonomous. Delegate via `codex-handoff` pattern. Money, purchase, plan change, or account delete is always human driven. Prompts must state that boundary verbatim.

## scope:verify (shared)

Read only plus the check command named in SPEC. Browser verify is headless via playwright MCP. Judge production UI on a production build, never on the dev server.

## scope:bench (eval harness)

Runs with `SOL_BACKEND=mock`. Scores trajectory, not prose. Asserts `final_state` against the store, never against the model summary. Categories map to the Kenward taxonomy subset: happy path, ambiguity, permission, scale, multi step, never do, injection.
