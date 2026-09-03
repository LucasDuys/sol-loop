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
