#!/usr/bin/env python3
"""Grade SWE slices forcing x86_64 for instances whose arm64 images are missing on the hub.

Usage: grade_x86.py <predictions.jsonl> <run_id>
Mutates swebench's USE_X86 set (read at spec build time) so the two pytest
instances below resolve x86_64 images under emulation instead of 404 arm64 pulls.
"""
import sys

FORCE_X86 = [
    "pytest-dev__pytest-7490",
    "pytest-dev__pytest-7571",
]

from swebench.harness.test_spec.test_spec import USE_X86

for iid in FORCE_X86:
    USE_X86.add(iid)

from swebench.harness.run_evaluation import main

main(
    dataset_name="princeton-nlp/SWE-bench_Verified",
    split="test",
    instance_ids=None,
    predictions_path=sys.argv[1],
    max_workers=2,
    force_rebuild=False,
    cache_level="env",
    clean=False,
    open_file_limit=4096,
    run_id=sys.argv[2],
    timeout=1800,
    namespace="swebench",
    rewrite_reports=False,
    modal=False,
)
