# Published scores (snapshots, approximate)

Dated leaderboard numbers to quote alongside our runs. Never quote without the date and the harness. Model-only scores are not agent scores: the scaffold moves results by 5 to 15 points on SWE-bench Verified.

## SWE-bench Verified (500 real GitHub issues, % resolved)

Snapshot September 2026, leaderboard at swebench.com plus September benchmark surveys:

| System | Score | Note |
|---|---|---|
| Claude Opus 5 | ~96% | leaderboard top, Sep 2026 |
| Claude Fable 5 | ~95% | vendor reported |
| GPT-5.5 | ~88.7% | vendor reported |
| Claude Opus 4.8 | ~88.6% | vendor reported |
| Qwen3.6-27B (open weights) | ~77.2% | API $0.60 / $3.60 per 1M |
| vexp plus Claude Code (100-task subset) | 73.0% at $0.67 per task | cost-efficient scaffold reference |
| OpenHands (same 100 subset) | 70.0% at $1.77 per task | scaffold reference |

SWE-bench Pro (contamination-resistant successor, 1,865 tasks): Claude Opus 4.8 ~69%, GPT-5.5 ~59%. Scores run 25 to 30 points below Verified.

## Other benchmarks

| Benchmark | Leader Sep 2026 | Note |
|---|---|---|
| Terminal-Bench 2.0 (89 Docker tasks) | GPT-5.5 ~82.7% | best shell-agent proxy |
| Aider polyglot (225 Exercism problems) | Claude Opus 4.5 ~89.4% | best cheap generation signal |
| HumanEval | 93 to 95% cluster | saturated, sanity floor only |

## Cost references

Full SWE-bench Verified run: about $25 compute plus 120 GB disk and 16 GB RAM. mini-SWE-agent defaults: 250 turns, $3 per task cap.
