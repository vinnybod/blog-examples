---
name: review
description: Run a code review using an alternate Claude instance (cz) against the z.ai endpoint. Use when you want a second opinion on code changes.
allowed-tools: Bash, Read, Grep, Glob
---

# CZ Code Review

Delegate a balanced code review to the `cz` instance (alternate model endpoint).

## Instructions

1. **Determine the review scope.** Check what has changed:
   - Run `git status` and `git diff --shortstat` to understand the scope
   - If the user passed `--base <ref>`, the review is a branch diff against that ref
   - Otherwise, review uncommitted working tree changes (staged + unstaged)

2. **Construct the task prompt.** Build a prompt for `cz` that tells it what to review. Include:
   - What to review: "Run `git diff` and `git diff --staged` to see all changes, then review them." or "Run `git diff <ref>...HEAD` to see the branch changes, then review them."
   - If the user provided focus text, include it: "Pay particular attention to: <focus>"
   - Tell it to check for: correctness, edge cases, error handling, potential bugs, and clarity

3. **Execute the review.** Run via Bash with a 300000ms timeout:

   ```bash
   ~/.claude/plugins/local/cz/scripts/invoke.sh \
     --system-prompt-file ~/.claude/plugins/local/cz/prompts/review.md \
     "<task prompt>"
   ```

4. **Handle errors.** If the command exits with a non-zero status or produces no output:
   - Report the error to the user
   - Show any stderr output
   - Do NOT try to interpret empty or error output as review findings

5. **Present the findings.** Interpret the `cz` response and present it to the user:
   - Summarize the key findings
   - Highlight any critical issues
   - Note if the review found no significant issues
