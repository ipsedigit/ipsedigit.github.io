---
name: work-on-branch
description: Use when working on a feature, fix, or experiment that should be previewed before going live — any work that does NOT go directly to production.
---

# Working on a Feature Branch

## Overview

Any branch other than `main` gets a live preview at `https://ipsedigit.github.io/{branch}` automatically on every push. Use branches to iterate safely before merging.

## Workflow

1. **Create or switch to your branch** (e.g. `git checkout -b my-feature`)
2. **Make changes, commit, push** — the `Deploy Preview` workflow triggers automatically
3. **Preview your changes** at `https://ipsedigit.github.io/{branch-name}` within ~2 minutes
4. **Iterate**: each push re-deploys the preview (clean deploy, previous preview overwritten)
5. **Merge to `main`** when satisfied — production deploys automatically
6. **Delete the branch** — the `Cleanup Preview` workflow removes `/{branch}` from the live site

## Branch Name → URL

The branch name is sanitized: slashes → `-`, underscores → `-`, uppercased → lowercased.

| Branch | Preview URL |
|---|---|
| `my-feature` | `ipsedigit.github.io/my-feature` |
| `fix/header` | `ipsedigit.github.io/fix-header` |
| `1` | `ipsedigit.github.io/1` |

## What the Workflow Does

- Checks out the branch
- Builds Jekyll with `--baseurl "/{branch}"` so all asset paths and links resolve correctly under the subfolder
- Deploys `_site/` to `gh-pages/{branch}/`
- Adds `.nojekyll` so GitHub Pages doesn't re-run Jekyll on the built output

## Rules

- **Never commit** — user commits manually
- The preview reflects the **last pushed commit**, not uncommitted local changes
- Previews are isolated: each branch has its own subfolder, they don't interfere with each other or with production
- The `gh-pages` branch is managed by automation — never push to it manually
