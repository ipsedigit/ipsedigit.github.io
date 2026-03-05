---
name: work-on-main
description: Use when making changes that should go directly to the live production site at ipsedigit.github.io.
---

# Working on Main

## Overview

`main` is production. Every push to `main` triggers a full Jekyll build and deploys the result live at `https://ipsedigit.github.io`. Changes are public within ~2 minutes of push.

## Workflow

1. **Make changes on `main`** (or merge a branch into it)
2. **Commit and push** — the `Deploy Production` workflow triggers automatically
3. **Site is live** at `https://ipsedigit.github.io` within ~2 minutes

## What the Workflow Does

- Builds Jekyll from `docs/` with `--baseurl ""` (no subfolder — root of the domain)
- Deploys `_site/` to the root of the `gh-pages` branch
- Adds `.nojekyll` so GitHub Pages doesn't re-run Jekyll on the built output
- Preserves all preview subdirectories (e.g. `gh-pages/1/`, `gh-pages/my-feature/`) — they are not deleted by production deploys

## When to Use Main Directly

- Hotfixes (typo, broken link, data update)
- News pipeline commits (automated daily publisher runs on `main`)
- Merging a reviewed branch

## When NOT to Use Main

- Structural changes to layouts, styles, or templates → use a branch first, preview at `/{branch}`, then merge
- Anything you're not confident about → branch first

## Rules

- **Never commit** — user commits manually
- The daily news pipeline (`dailynewspublisher.yml`) commits directly to `main` automatically — don't interfere with it
- The `gh-pages` branch is managed by automation — never push to it manually
