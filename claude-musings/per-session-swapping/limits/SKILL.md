---
name: limits
description: Show Claude and z.ai rate limit usage with colored visual bars
disable-model-invocation: true
allowed-tools: Bash
---

# Usage Limits

Run this command:

```
python3 ~/.claude/skills/limits/show-limits.py
```

**CRITICAL**: The script outputs beautifully formatted ANSI-colored text that the user can already see in the Bash tool output. After running the command, your ONLY response must be an empty message or at most a single word like "Done." Do NOT:
- Restate, summarize, or reformat the output
- Add a table, code block, or plain-text version of the same data
- Add commentary about the results (e.g. "Your Claude usage is high")
- Explain what the numbers mean

The user can see the colored output directly. Any repetition is noise.
