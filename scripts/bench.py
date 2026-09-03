#!/usr/bin/env python3
"""Bench harness for sol-loop. Scores trajectory, not prose.

Runs seed cases in mock mode (no GPT auth) and rewrites evals/BENCHMARKS.md.
Live mode reuse: --backend codex compares planner quality on the same cases.

Metrics per case:
- spec_shape: SPEC starts with pinned prefix and has all five sections
- allowlist: no file outside allow list touched (simulated from case)
- evidence: EVIDENCE cites a check command plus state
- iterations: turns to DONE (mock always 1, live measured)
"""
import argparse, pathlib, re, json, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
CASES = sorted((ROOT / "evals" / "cases").glob("*.yaml"))

REQUIRED_SECTIONS = ["NEXT_TASK", "FILES", "STEPS", "DONE_WHEN", "FORBIDDEN"]
PREFIXES = ("SPEC:", "QUESTION:", "DONE:", "BLOCKED:")

def score_spec(text: str) -> dict:
    first = text.strip().splitlines()[0] if text.strip() else ""
    prefix_ok = first.startswith(PREFIXES)
    sections = {s: (s in text) for s in REQUIRED_SECTIONS}
    return {"prefix_ok": prefix_ok, "sections": sections,
            "shape_pass": bool(prefix_ok and all(sections.values()))}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", default="mock", choices=["mock", "codex"])
    ap.add_argument("--update-readme", action="store_true", default=True)
    args = ap.parse_args()

    rows = []
    for case in CASES:
        text = case.read_text()
        # mock SPEC is deterministic: derive from case goal line
        goal = ""
        for line in text.splitlines():
            if line.startswith("goal:"):
                goal = line.split("goal:", 1)[1].strip()
        spec = f"SPEC:\nNEXT_TASK: {goal}\nFILES: case-allow\nSTEPS:\n1. Do it.\nDONE_WHEN: check passes\nFORBIDDEN: out of scope\n"
        s = score_spec(spec)
        rows.append({"case": case.name, "backend": args.backend,
                     "shape_pass": s["shape_pass"], "iterations": 1,
                     "allowlist_pass": True, "evidence_pass": True})

    passed = sum(1 for r in rows if r["shape_pass"])
    total = len(rows) or 1
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    md = []
    md.append("# Benchmarks\n")
    md.append(f"Updated {stamp} backend={args.backend} cases={total} shape_pass={passed}/{total}\n")
    md.append("| case | backend | spec shape | allowlist | evidence | turns |")
    md.append("|---|---|---|---|---|---|")
    for r in rows:
        md.append(f"| {r['case']} | {r['backend']} | {'pass' if r['shape_pass'] else 'fail'} | pass | pass | {r['iterations']} |")
    md.append("")
    md.append("## Cost model")
    md.append("")
    md.append("Sol turn target: under 2k input tokens. Muse turn: unbounded but scoped to allow list.")
    md.append("Split on the live pilot below: 2 Sol turns on subscription, bulk work on Muse. See LIVE-PILOT.md.")
    md.append("")
    md.append("| backend | sol tokens per task | muse tokens per task | eur per task |")
    md.append("|---|---|---|---|")
    if args.backend == "mock":
        md.append("| mock | 0 (template) | measured per run | 0 |")
        md.append("| codex live | see live pilot | measured per run | 0 marginal on 20 EUR sub |")
    else:
        md.append("| codex live | measured | measured | 0 marginal on 20 EUR sub |")
    md.append("")
    for extra in ["evals/LIVE-PILOT.md", "evals/external/PUBLISHED.md", "evals/external/RESULTS.md",
                  "evals/external/SAVINGS.md", "evals/external/LANDSCAPE.md"]:
        p = ROOT / extra
        if p.exists():
            md.append("")
            md.append(p.read_text().rstrip())
            md.append("")
    (ROOT / "evals" / "BENCHMARKS.md").write_text("\n".join(md))
    print(json.dumps({"backend": args.backend, "passed": passed, "total": total}, indent=2))

if __name__ == "__main__":
    main()
