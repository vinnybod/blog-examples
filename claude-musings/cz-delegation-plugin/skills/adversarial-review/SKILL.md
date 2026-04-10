---
name: adversarial-review
description: Run an adversarial code review using an alternate Claude instance (cz) that aggressively challenges design choices, tradeoffs, and assumptions. Use when you want a skeptical second opinion.
allowed-tools: Bash, Read, Grep, Glob
---

# CZ Adversarial Review

Delegate an adversarial code review to the `cz` instance (alternate model endpoint). This review defaults to skepticism and actively tries to break confidence in the change.

## Instructions

1. **Determine the review scope.** Check what has changed:
   - Run `git status` and `git diff --shortstat` to understand the scope
   - If the user passed `--base <ref>`, the review is a branch diff against that ref
   - Otherwise, review uncommitted working tree changes (staged + unstaged)

2. **Parse user focus.** If the user provided additional text after the command (e.g., `/cz:adversarial-review look for race conditions`), capture it as the focus area.

3. **Construct the task prompt.** Build a prompt for `cz` that tells it what to review:
   - What to review: "Run `git diff` and `git diff --staged` to see all changes, then review them." or "Run `git diff <ref>...HEAD` to see the branch changes, then review them."
   - If the user provided focus text: "Pay particular attention to: <focus>"

4. **Execute the review.** Run via Bash with a 300000ms timeout:

   ```bash
   ~/.claude/plugins/local/cz/scripts/invoke.sh \
     --system-prompt-file ~/.claude/plugins/local/cz/prompts/adversarial-review.md \
     "<task prompt>"
   ```

5. **Handle errors.** If the command exits with a non-zero status or produces no output:
   - Report the error to the user
   - Show any stderr output
   - Do NOT try to interpret empty or error output as review findings

6. **Present the findings.** Interpret the `cz` response and present it to the user:
   - Lead with the verdict (APPROVE or NEEDS-ATTENTION)
   - List findings by severity, highest first
   - For each finding, highlight: the affected file/lines, what can go wrong, and the recommended fix
   - End with next steps
