#!/bin/zsh
# Router for sol-loop. Code enforces what prose states.
# Usage: SOL_BACKEND=mock|codex scripts/run.sh --goal GOAL.md --allow allow.txt [--workdir .] [--max-turns 5]
set -euo pipefail

BACKEND="${SOL_BACKEND:-mock}"
# Empty SOL_MODEL means use the model in ~/.codex/config.toml.
# On this machine that is gpt-5.6-sol with model_reasoning_effort xhigh.
MODEL="${SOL_MODEL:-}"
GOAL=""; ALLOW=""; WORKDIR="."; MAX_TURNS=5

while [[ $# -gt 0 ]]; do
  case "$1" in
    --goal) GOAL="$2"; shift 2;;
    --allow) ALLOW="$2"; shift 2;;
    --workdir) WORKDIR="$2"; shift 2;;
    --max-turns) MAX_TURNS="$2"; shift 2;;
    *) echo "unknown arg $1"; exit 2;;
  esac
done

[[ -z "$GOAL" || -z "$ALLOW" ]] && { echo "usage: run.sh --goal GOAL.md --allow allow.txt"; exit 2; }
[[ -f "$GOAL" ]] || { echo "missing goal $GOAL"; exit 2; }
[[ -f "$ALLOW" ]] || { echo "missing allow list $ALLOW"; exit 2; }

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STATE_DIR="$WORKDIR/.sol-loop"
mkdir -p "$STATE_DIR"
EVIDENCE="$STATE_DIR/EVIDENCE.md"
SPEC="$STATE_DIR/SPEC.md"
[[ -f "$EVIDENCE" ]] || echo "none yet" > "$EVIDENCE"

GOAL_TEXT="$(cat "$GOAL")"
ALLOW_TEXT="$(cat "$ALLOW")"

turn=1
while [[ $turn -le $MAX_TURNS ]]; do
  EVID_TEXT="$(cat "$EVIDENCE")"
  if [[ "$BACKEND" == "codex" ]]; then
    PROMPT_FILE="$STATE_DIR/sol-prompt-$turn.md"
    {
      echo "You are a planner. Goal:"; echo "$GOAL_TEXT"
      echo "Evidence:"; echo "$EVID_TEXT"
      echo "Allow list:"; echo "$ALLOW_TEXT"
      echo "Planner contract: $(cat "$ROOT/agents/sol-planner.md")"
    } > "$PROMPT_FILE"
    if [[ -n "$MODEL" ]]; then
      codex exec --skip-git-repo-check -s read-only -C "$WORKDIR" -m "$MODEL" "$(cat "$PROMPT_FILE")" | tee "$SPEC"
    else
      codex exec --skip-git-repo-check -s read-only -C "$WORKDIR" "$(cat "$PROMPT_FILE")" | tee "$SPEC"
    fi
  else
    "$ROOT/scripts/mock-sol.sh" --goal "$GOAL" --evidence "$EVIDENCE" --allow "$ALLOW" | tee "$SPEC"
  fi

  HEAD_LINE="$(head -n 1 "$SPEC")"
  case "$HEAD_LINE" in
    DONE:*|BLOCKED:*|QUESTION:*)
      echo "router: Sol returned $HEAD_LINE"
      exit 0;;
    SPEC:*|"WORKING:"*|*)
      echo "router: executing SPEC turn $turn";;
  esac

  echo "router: executor step is manual in this version. Implement your SPEC, then append EVIDENCE to $EVIDENCE and re run."
  echo "router: wrote $SPEC. Next: run executor agent with agents/muse-executor.md, then $ROOT/scripts/check-allowlist.sh --allow $ALLOW --workdir $WORKDIR"
  exit 3
done
