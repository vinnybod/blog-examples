---
name: ask
description: Get a second opinion from an alternate Claude instance (cz) on any question. Use when you want an independent perspective on architecture, design, implementation, or debugging.
allowed-tools: Bash, Read, Grep, Glob
---

# CZ Ask

Get a second opinion from the `cz` instance (alternate model endpoint) on any question.

## Instructions

1. **Parse the question.** The user's text after `/cz:ask` is the question. It may be a direct question, a request for advice, or a prompt for analysis.

2. **Construct a context bundle.** Use your judgment to decide what context `cz` needs to answer the question well. Guidelines:
   - If the question references specific files → include their paths in the task prompt so `cz` can read them
   - If the question is about recent changes → mention that `cz` should look at the git diff
   - If the question builds on the current conversation → summarize the relevant conversation context (what you've been working on, decisions made, current state)
   - If the question is a general architecture/design question → just pass the question, `cz` can explore the repo as needed

3. **Construct the task prompt.** Combine the question with the context bundle into a clear task prompt for `cz`.

4. **Execute.** Run via Bash with a 300000ms timeout:

   ```bash
   ~/.claude/plugins/local/cz/scripts/invoke.sh \
     --system-prompt-file ~/.claude/plugins/local/cz/prompts/ask.md \
     "<task prompt with context>"
   ```

5. **Handle errors.** If the command exits with a non-zero status or produces no output:
   - Report the error to the user
   - Show any stderr output
   - Do NOT try to interpret empty or error output

6. **Present the response.** Interpret the `cz` response and present it to the user:
   - Summarize the key points of `cz`'s opinion
   - Note where `cz` agrees or disagrees with the approach the current session has been taking
   - If `cz` raises concerns, highlight them clearly
