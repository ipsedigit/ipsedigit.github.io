---
name: update-claude-md
description: Use when a work session produces significant changes to project structure, architecture, active features, file layout, or development conventions — before the session ends or a major task completes.
---

# Update CLAUDE.md

## Overview

CLAUDE.md is the persistent project memory loaded into every session. It must reflect the current state of the project, not a historical snapshot. Update it whenever the project changes meaningfully.

## When to Trigger

**Do update after:**
- A feature is added or removed (new Python module, new workflow, new Jekyll section)
- Files are renamed, moved, or deleted in ways that affect the architecture map
- A new convention is established (naming, tooling, workflow)
- The project's purpose or scope shifts
- A significant pruning or cleanup session (like today's)

**Do NOT update for:**
- Bug fixes that don't change structure
- Style-only edits
- Content changes (new news posts, data file updates)
- Anything already accurately described in CLAUDE.md

## How to Update

1. **Read CLAUDE.md first** — never rewrite from scratch
2. **Identify only what changed** — be surgical, not comprehensive
3. **Edit the relevant section(s)** — use the Edit tool, not Write
4. **Keep it concise** — CLAUDE.md is loaded into every session; every line costs context

## Sections and What Triggers Each

| Section | Update when... |
|---|---|
| **Architecture** code block | Files added/removed/renamed in the pipeline or docs/ |
| **Five Niches** | Niches added or removed from `NICHE_CATEGORIES` |
| **Conventions** | New rule established, old rule changed |
| **Current State** | Features pruned or added; project direction shifts |
| **Development Philosophy** | New principle adopted after reflection |

## Rules

- **Never auto-commit** — user commits manually
- **Edit minimally** — change only what's inaccurate, leave the rest
- **Date the state** — if updating "Current State", note the date of the change
- **No speculation** — only write what is confirmed, not what is planned

## Example

After removing the Digest feature:

```
# Before
- digest.py → weekly digest generator

# After (remove that line; update Current State)
## Current State (post-cleanup, 2026-03-04)
Digest removed. What remains: news pipeline + Jekyll front-end.
```
