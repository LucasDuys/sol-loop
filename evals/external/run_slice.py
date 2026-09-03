#!/usr/bin/env python3
"""Slice runner for sol-loop external benchmarks. Stdlib only, except --swe-ids needs `datasets`.

Prepare: runs the planner per task (timed, Sol units parsed), writes executor manifest.
Grade: runs each task check, writes results.jsonl and updates RESULTS.md comparison table.
Collect-patches: emits SWE-bench predictions JSONL from task workdirs for the official harness.
"""
import argparse, json, pathlib, re, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
RUN_SH = ROOT / "scripts" / "run.sh"
PREFIXES = ("SPEC:", "QUESTION:", "DONE:", "BLOCKED:")
REQUIRED_SECTIONS = ["NEXT_TASK", "FILES", "STEPS", "DONE_WHEN", "FORBIDDEN"]


def parse_sol_units(log_text: str):
    units = re.findall(r"tokens used\s*\n?\s*([0-9]+(?:\.[0-9]+)?)", log_text)
    return units[-1] if units else "n/a"


def spec_shape_ok(spec_text: str) -> bool:
    lines = spec_text.strip().splitlines()
    if not lines or not lines[0].startswith(PREFIXES):
        return False
    return all(s in spec_text for s in REQUIRED_SECTIONS)


def prepare_task(task: dict, out_dir: pathlib.Path, harness: str, backend: str) -> dict:
    tdir = out_dir / task["id"]
    wdir = tdir / "work"
    wdir.mkdir(parents=True, exist_ok=True)
    for rel, content in task.get("files", {}).items():
        p = wdir / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    (tdir / "GOAL.md").write_text(task["goal"])
    (tdir / "allow.txt").write_text("\n".join(task.get("allow", ["*"])) + "\n")
    rec = {"id": task["id"], "harness": harness, "backend": backend,
           "planner_wall_s": 0, "sol_units": "n/a", "spec_shape": "n/a", "status": "awaiting-executor"}
    if harness == "sol-loop":
        t0 = time.time()
        log = tdir / "planner.log"
        cmd = ["zsh", str(RUN_SH), "--goal", str(tdir / "GOAL.md"),
               "--allow", str(tdir / "allow.txt"), "--workdir", str(wdir)]
        import os as _os
        env = dict(_os.environ)
        env["SOL_BACKEND"] = backend
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=600, env=env)
            log.write_text((p.stdout or "") + "\n" + (p.stderr or ""))
        except subprocess.TimeoutExpired:
            log.write_text("TIMEOUT after 600s")
        rec["planner_wall_s"] = round(time.time() - t0, 1)
        spec = tdir / "work" / ".sol-loop" / "SPEC.md"
        rec["sol_units"] = parse_sol_units(log.read_text())
        rec["spec_shape"] = "pass" if spec.exists() and spec_shape_ok(spec.read_text()) else "fail"
        rec["status"] = "awaiting-executor"
        (tdir / "manifest.json").write_text(json.dumps(
            {"executor_input": str(spec) if spec.exists() else "planner failed, see planner.log",
             "prompt": "agents/muse-executor.md", "check": task.get("check", "")}, indent=2))
    else:
        (tdir / "BRIEF.md").write_text(
            task["goal"] + "\n\nAllowed files: " + ", ".join(task.get("allow", ["*"])) +
            "\nCheck: " + task.get("check", "") + "\n")
        (tdir / "manifest.json").write_text(json.dumps(
            {"executor_input": str(tdir / "BRIEF.md"),
             "prompt": "implement directly, no SPEC", "check": task.get("check", "")}, indent=2))
    (tdir / "record.json").write_text(json.dumps(rec, indent=2))
    return rec


def grade_run(run_dir: pathlib.Path) -> list:
    results = []
    for tdir in sorted(run_dir.iterdir()):
        rec_path = tdir / "record.json"
        if not tdir.is_dir() or not rec_path.exists():
            continue
        rec = json.loads(rec_path.read_text())
        task_check = json.loads((tdir / "manifest.json").read_text()).get("check", "")
        passed = False
        detail = "no check"
        if task_check:
            try:
                p = subprocess.run(task_check, shell=True, capture_output=True, text=True,
                                   timeout=300, cwd=str(tdir / "work"))
                passed = p.returncode == 0
                tail = ((p.stdout or "") + (p.stderr or "")).strip().splitlines()
                detail = " | ".join(tail[-3:]) if tail else "no output"
            except subprocess.TimeoutExpired:
                detail = "TIMEOUT after 300s"
        rec.update({"pass": passed, "check_detail": detail[:200], "status": "graded"})
        rec_path.write_text(json.dumps(rec, indent=2))
        results.append(rec)
    results_path = run_dir / "results.jsonl"
    with results_path.open("w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    return results


def update_results_md(run_dir: pathlib.Path, results: list):
    md_path = ROOT / "evals" / "external" / "RESULTS.md"
    passed = sum(1 for r in results if r.get("pass"))
    lines = [f"### {run_dir.name} ({results[0]['harness'] if results else 'empty'}, backend {results[0]['backend'] if results else 'n/a'})",
             "", f"pass {passed}/{len(results)}", "",
             "| task | pass | spec shape | planner s | sol units | check detail |",
             "|---|---|---|---|---|---|"]
    for r in results:
        lines.append(f"| {r['id']} | {'pass' if r.get('pass') else 'fail'} | {r.get('spec_shape')} | "
                     f"{r.get('planner_wall_s')} | {r.get('sol_units')} | {r.get('check_detail', '')} |")
    lines += ["", ""]
    existing = md_path.read_text() if md_path.exists() else "# External results\n\nNo external runs yet.\n\n"
    if "No external runs yet." in existing:
        existing = "# External results\n\nSol-loop vs muse-only on the same slices, plus dated leaderboard quotes in PUBLISHED.md.\n\n"
    md_path.write_text(existing.rstrip() + "\n\n" + "\n".join(lines))


def cmd_prepare(args):
    tasks = [json.loads(l) for l in pathlib.Path(args.tasks).read_text().splitlines() if l.strip()]
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    recs = [prepare_task(t, out, args.harness, args.backend) for t in tasks]
    print(json.dumps({"run": str(out), "harness": args.harness, "backend": args.backend,
                      "tasks": len(recs),
                      "spec_shape_pass": sum(1 for r in recs if r["spec_shape"] == "pass")}, indent=2))
    print(f"next: execute each {out}/<id>/ per its manifest.json, then grade with --grade {out}")


def cmd_swe(args):
    from datasets import load_dataset
    ds = {r["instance_id"]: r for r in load_dataset("princeton-nlp/SWE-bench_Verified", split="test")}
    ids = [l.strip() for l in pathlib.Path(args.swe_ids).read_text().splitlines() if l.strip()]
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for iid in ids:
        inst = ds[iid]
        task = {"id": iid, "goal": inst["problem_statement"], "allow": ["*"],
                "files": {}, "check": "official harness grades this task",
                "repo": inst["repo"], "base_commit": inst["base_commit"]}
        tdir = out / iid
        (tdir / "work").mkdir(parents=True, exist_ok=True)
        repo_url = f"https://github.com/{inst['repo']}.git"
        wdir = tdir / "work" / "repo"
        if not (wdir / ".git").exists():
            subprocess.run(["git", "clone", repo_url, str(wdir)], check=True)
        subprocess.run(["git", "-C", str(wdir), "fetch", "origin", inst["base_commit"]],
                       check=True, capture_output=True)
        subprocess.run(["git", "-C", str(wdir), "checkout", inst["base_commit"]],
                       check=True, capture_output=True)
        prepare_task(task, out, args.harness, args.backend)
    print(f"swe slice ready at {out}. Scope enforcement is OFF (allow *), recorded per task.")


def cmd_collect(args):
    run_dir = pathlib.Path(args.collect_patches)
    for tdir in sorted(run_dir.iterdir()):
        repo = tdir / "work" / "repo"
        if (repo / ".git").exists():
            p = subprocess.run(["git", "-C", str(repo), "diff"], capture_output=True, text=True)
            if p.stdout.strip():
                print(json.dumps({"instance_id": tdir.name, "model_patch": p.stdout,
                                  "model_name_or_path": "sol-loop"}))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks")
    ap.add_argument("--swe-ids")
    ap.add_argument("--harness", default="sol-loop", choices=["sol-loop", "muse-only"])
    ap.add_argument("--backend", default="mock", choices=["mock", "codex"])
    ap.add_argument("--out")
    ap.add_argument("--grade")
    ap.add_argument("--collect-patches")
    args = ap.parse_args()
    if args.collect_patches:
        return cmd_collect(args)
    if args.grade:
        results = grade_run(pathlib.Path(args.grade))
        update_results_md(pathlib.Path(args.grade), results)
        print(json.dumps({"graded": len(results),
                          "passed": sum(1 for r in results if r.get("pass"))}, indent=2))
        return
    if args.swe_ids:
        return cmd_swe(args)
    if not args.tasks or not args.out:
        sys.exit("need --tasks plus --out, or --swe-ids, or --grade, or --collect-patches")
    return cmd_prepare(args)


if __name__ == "__main__":
    main()
