# Savings math

How much less Sol you burn with the loop, and what that is worth. Measured numbers are measured. Modeled numbers are labeled and show their assumptions.

## The one honest paragraph

Both setups ride your flat 20 EUR subscription at 0 EUR marginal, so today's actual bill saves 0%. The scarce resource is the usage limit, and there the loop wins: planning costs ~9 units per task flat, implementing directly cost ~12 units on a 5 line function and the bill grows with task size. Money savings appear the moment the alternative is metered: API pricing or a Pro upgrade to lift limits.

## Measured (smoke slice, Sep 2026)

| | sol-loop planner | sol-only implement |
|---|---|---|
| Subscription units per trivial task | 9.1 | 12.2 |
| Wall per task | 10.4s | 29.3s |
| Rate limited runs | 0 of 6 | 5 of 6 |

Unit saving on trivial tasks: about 25%. The saving grows with task size because planning is O(goal) while implementing is O(repo). A 5 line function barely separates them. A multi file fix with reads, iterations, and verification is where the split pays.

## Modeled (mid size task, metered API alternative)

Assumptions: 1 subscription unit is about 1k tokens. Executor bulk for a mid size task is about 40k input plus 8k output tokens. Planner is about 8k input plus 1k output. Prices: GPT-5.5 at $5 / $30 per 1M input / output tokens, Sep 2026 published.

| | All on metered model | sol-loop (planner metered, executor on Muse) |
|---|---|---|
| Executor bulk | ~$0.44 | ~$0.00 |
| Planning | included above | ~$0.07 |
| Per task | ~$0.51 | ~$0.07 |
| 20 tasks a day, 22 days | ~$225 / month | ~$31 / month |

Saving: about 85% of metered spend per task, about $195 / month at that volume. Against frontier metered models the percentage holds and the absolute gap is larger. Against your current flat sub plus free Muse the bill is 20 EUR either way and the saving is throughput per limit window, roughly 3x on unit cost alone before counting that planner calls fit where implement runs get cut off.

## What would change these numbers

A 20 task Exercism slice through both arms pins the unit curve across difficulty. A 10 task SWE-bench Verified slice pins accuracy per unit, which is the number that decides routing vs Fable. Both are wired in `evals/external/`.
