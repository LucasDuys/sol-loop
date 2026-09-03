#!/bin/zsh
# One command install for sol-loop. Idempotent, safe to re run.
# Usage: ./install.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
OCFG="$HOME/.config/opencode"
AGENTS="$OCFG/agents"
SKILLS="$OCFG/skills"

mkdir -p "$AGENTS" "$SKILLS" "$HOME/.local/bin"

ln -sfn "$ROOT" "$SKILLS/sol-loop"
ln -sfn "$ROOT/agents/muse-executor.md" "$AGENTS/muse-executor.md"
ln -sfn "$ROOT/agents/sol-planner.md" "$AGENTS/sol-planner.md"
ln -sfn "$ROOT/scripts/sol-loop" "$HOME/.local/bin/sol-loop"
chmod +x "$ROOT/scripts/"*.sh "$ROOT/scripts/sol-loop" "$ROOT/install.sh"

echo "linked: $SKILLS/sol-loop -> $ROOT"
echo "linked: $AGENTS/muse-executor.md"
echo "linked: $AGENTS/sol-planner.md"
echo "linked: ~/.local/bin/sol-loop"

if command -v codex >/dev/null 2>&1; then
  if codex exec --skip-git-repo-check -s read-only -C "$HOME" "reply with exactly OK" 2>/dev/null | grep -q "OK"; then
    echo "codex: auth OK, live planner available"
  else
    echo "codex: no auth, mock mode only. Run: codex auth login"
  fi
else
  echo "codex: CLI not found, mock mode only"
fi

python3 "$ROOT/scripts/bench.py" --backend mock >/dev/null
echo "bench: seed evals pass, see evals/BENCHMARKS.md"
echo ""
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
  echo "note: add ~/.local/bin to PATH, then run: sol-loop --goal GOAL.md --allow allow.txt"
else
  echo "next: cd your-repo && sol-loop --goal GOAL.md --allow allow.txt"
fi
