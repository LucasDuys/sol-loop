#!/bin/zsh
# L2 enforcement: reject diffs outside the allow list. Code decides, not prose.
# Usage: check-allowlist.sh --allow allow.txt [--workdir .]
set -euo pipefail
ALLOW=""; WORKDIR="."
while [[ $# -gt 0 ]]; do
  case "$1" in
    --allow) ALLOW="$2"; shift 2;;
    --workdir) WORKDIR="$2"; shift 2;;
    *) echo "unknown arg $1"; exit 2;;
  esac
done
[[ -z "$ALLOW" ]] && { echo "usage: check-allowlist.sh --allow allow.txt"; exit 2; }
cd "$WORKDIR"
if ! git rev-parse --git-dir >/dev/null 2>&1; then echo "allowlist: not a git repo, skip"; exit 0; fi
CHANGED="$(git status --porcelain | awk '{print $2}')"
[[ -z "$CHANGED" ]] && { echo "allowlist: clean tree, pass"; exit 0; }
FAIL=0
while IFS= read -r f; do
  [[ -z "$f" ]] && continue
  if ! grep -qxF "$f" "$ALLOW" && ! grep -q "^\*$" "$ALLOW"; then
    # prefix match: allow list may contain directories
    OK=0
    while IFS= read -r a; do
      [[ -z "$a" ]] && continue
      case "$f" in "$a"* ) OK=1; break;; esac
    done < "$ALLOW"
    if [[ $OK -eq 0 ]]; then echo "allowlist: REJECT $f not in $ALLOW"; FAIL=1; fi
  fi
done <<< "$CHANGED"
[[ $FAIL -eq 1 ]] && exit 1
echo "allowlist: pass"
