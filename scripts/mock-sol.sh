#!/bin/zsh
# Mock Sol for pre auth use. Emits a SPEC from goal plus evidence without calling GPT.
# Usage: mock-sol.sh --goal GOAL.md --evidence EVIDENCE.md --allow allow.txt
set -euo pipefail
GOAL=""; EVIDENCE=""; ALLOW=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --goal) GOAL="$2"; shift 2;;
    --evidence) EVIDENCE="$2"; shift 2;;
    --allow) ALLOW="$2"; shift 2;;
    *) echo "unknown arg $1"; exit 2;;
  esac
done
GOAL_TEXT="$(cat "$GOAL")"
ALLOW_TEXT="$(cat "$ALLOW" | head -n 20)"
cat <<EOF
SPEC:
NEXT_TASK: $GOAL_TEXT
FILES: $ALLOW_TEXT
STEPS:
1. Read the listed files. Change only what the goal requires.
2. Run the repo check for the touched package.
3. Append raw check output to .sol-loop/EVIDENCE.md.
DONE_WHEN: repo check for touched package passes plus git status --short shows only allow listed paths
FORBIDDEN: files outside the allow list, live facing restyle as side effect, secrets in chat
EOF
