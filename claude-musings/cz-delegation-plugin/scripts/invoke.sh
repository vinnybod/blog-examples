#!/bin/bash
set -euo pipefail

# Wrapper for invoking cz (alternate Claude instance) in print mode
# with read-only tools and auto-approved permissions.
#
# Usage:
#   invoke.sh [--system-prompt-file <path>] <task prompt>
#
# Options:
#   --system-prompt-file  Path to a file containing the system prompt to append.
#                         If omitted, no system prompt is appended.
#
# The task prompt is the final positional argument.

SYSTEM_PROMPT_FILE=""

while [[ $# -gt 1 ]]; do
  case "$1" in
    --system-prompt-file)
      SYSTEM_PROMPT_FILE="$2"
      shift 2
      ;;
    *)
      break
      ;;
  esac
done

TASK_PROMPT="${1:?Usage: invoke.sh [--system-prompt-file <path>] <task prompt>}"

CZ_ARGS=(
  -p
  --allowed-tools "Read,Grep,Glob,Bash(git:*)"
  --permission-mode dontAsk
)

if [[ -n "$SYSTEM_PROMPT_FILE" ]]; then
  if [[ ! -f "$SYSTEM_PROMPT_FILE" ]]; then
    echo "Error: system prompt file not found: $SYSTEM_PROMPT_FILE" >&2
    exit 1
  fi
  CZ_ARGS+=(--append-system-prompt "$(cat "$SYSTEM_PROMPT_FILE")")
fi

CZ_ARGS+=("$TASK_PROMPT")

exec cz "${CZ_ARGS[@]}" < /dev/null
