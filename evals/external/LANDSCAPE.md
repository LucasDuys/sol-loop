# Benchmark landscape 2026

The popular coding benchmarks people actually run, what each proves, and where sol-loop stands on it. Snapshot September 2026.

## Headline benchmarks

| Benchmark | What it proves | Size | Frontier Sep 2026 | Cost to run | sol-loop status |
|---|---|---|---|---|---|
| SWE-bench Verified | Real GitHub issues, multi file patch, no regressions | 500 Python tasks | ~89 to 96% | ~$25 compute, 120 GB disk, Docker | 10-slice wired, not yet run |
| SWE-bench Pro | Same idea, private repos, contamination resistant | 1,865 tasks | ~59 to 69% | heavy | quote only |
| Terminal-Bench 2.0 | Shell living agent, Docker terminal tasks | 89 tasks | ~82.7% (GPT-5.5) | Docker, Linux | quote only |
| LiveCodeBench | Code generation from spec, rolling cutoff | rolling | top Elo Gemini 3.1 Pro | custom harness | quote only |
| Aider polyglot | Function from spec, 6 languages | 225 Exercism tasks | ~89.4% (Opus 4.5) | cents, no Docker | 20-slice planned, 6 task smoke passing |
| SWE-bench Multilingual | Verified across 9 languages | 300 tasks | varies by lang | Docker | quote only |

## Retired as comparisons

HumanEval and MBPP: saturated at 93 to 95% since 2024, contaminated. Sanity floor only. BigCodeBench: saturating, complement at best.

## What to quote together

One benchmark never tells the story. The honest claim pairs at least two: SWE-bench Verified for engineering plus Terminal-Bench or polyglot for breadth, with the harness disclosed. Model-only scores are not agent scores: scaffolds move Verified results 5 to 15 points.

## Cost references

Efficient scaffolds on a 100 task Verified subset: $0.67 to $1.77 per task. Frontier API models: roughly $100k to $500k per 10M output tokens per month at team scale. Flat subscriptions (Codex 20 EUR, Claude Pro): marginal euros are zero, the scarce resource is rate limits and wall time. That is the tradeoff sol-loop is built for: move bulk tokens off the metered model and off the rate limited planner.
