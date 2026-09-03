## Live pilot 2026-09-03

Demo goal in `/tmp/sol-loop-demo`: add exported `greet` returning `hello sol` to `hello.ts`, allow list `hello.ts` only.

- Turn 1 Sol (`gpt-5.6-sol` xhigh, subscription): `SPEC:` with NEXT_TASK, FILES, STEPS, DONE_WHEN, FORBIDDEN. Codex reported tokens used `9.267`.
- Executor (Muse Spark): 1 read plus 1 edit plus 1 check plus evidence write. Check `node --experimental-strip-types ...` printed exactly `hello sol`.
- Turn 2 Sol: `DONE:` citing the check output. Codex reported tokens used `8.886`.
- Allow list: only source file touched was `hello.ts`. No tracked diffs outside scope.
- Cost: both Sol turns on the 20 EUR subscription at 0 EUR marginal. Executor tokens on Muse. Split matches the design: Sol under 20 subscription units per task, bulk work on Muse.
