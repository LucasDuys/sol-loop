# Routing: what to send where

Measured on the smoke slice Sep 2026, plus principle where noted. Numbers are small slice, direction matters more than digits.

## Measured

- Sol planner SPEC: ~9 subscription units and ~10s per task, flat. SPEC cost scales with goal plus evidence size, not repo size.
- Sol implementing directly (1 clean run): ~12 units and ~29s for a 5 line function. Reads plus edits plus verification all ride the subscription.
- Muse executing from SPEC or brief: 6/6 on smoke tasks either way. Executor quality held constant, planner is the variable.
- Rate limit event: 5 of 6 sol-only runs died with `usage limit, try again at 2:24 PM` after a morning of planning calls. Small planner calls fit many more per window than full implement runs.

## Rules

Send to sol-loop when the task is scoped and verifiable: multi file edits, bug fixes with a failing test, migrations with checks, UI work inside an allow listed area. Planning cost stays flat while execution bulk rides Muse. This is also the under pressure default: when Sol is rate limited, planner calls still fit and executor calls cost nothing.

Send to Sol directly when the task is smaller than the SPEC overhead: single file trivial edits, quick probes, DONE decisions on evidence. Measured overhead is about 10s plus 9 units before any work happens.

Send to Fable (frontier API, metered) when accuracy beats cost: novel architecture, ambiguous product calls, the hardest bugs, anything unscoped where a wrong patch costs more than tokens. No Fable numbers measured here; published SWE-bench Verified runs ~89 to 96% at team scale API cost. Use it as the escalation tier, not the default.

## The economy in one line

Planning cost is O(goal). Execution cost is O(repo). sol-loop puts the first on the flat subscription and the second on Muse. Direct Sol pays both on the subscription and dies first under rate limits, as measured.
