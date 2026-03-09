---
name: build-new-section
description: Use when adding a new page/section to eof.news reachable from the site header — a page backed by a Python data generator, a JSON data file, a Liquid layout, and a nav link.
---

# build-new-section

## Overview

A **section** is a new page reachable from the site header, styled consistently with the homepage, and fed by a dedicated Python script that fetches/computes content from its own sources and writes a `docs/_data/<section>.json` file consumed by a Liquid layout.

Every section has four layers: **Python generator → JSON data → Liquid layout → landing page + nav link**.

---

## Checklist

Work top-to-bottom. All steps are required.

### 1. Python generator (`<section>.py`)

- Create `<section>.py` at repo root (same level as `news.py`)
- Entry point: a single `publish_<section>()` function
- Write output to `docs/_data/<section>.json` with a `generated_at` ISO timestamp
- **No external deps** beyond stdlib + `feedparser`, `bs4`, `requests`
- Register in `main.py`:
  ```python
  case "<section>":
      from <section> import publish_<section>
      publish_<section>()
  ```

### 2. JSON data file (`docs/_data/<section>.json`)

- Output path: `docs/_data/<section>.json`
- Structure:
  ```json
  {
    "items": [...],
    "generated_at": "2026-03-09T12:00:00+00:00"
  }
  ```
- Accessed in Liquid as `site.data.<section>.items`
- Keep field names simple and consistent

### 3. Layout (`docs/_layouts/<section>.html`)

- Start with `layout: base` (never duplicate the `<html>` scaffold)
- Consume data via `site.data.<section>.items`
- **Reuse existing CSS classes** — `post-item`, `post-meta`, `niche-badge`, `tag`, etc. — before writing any new CSS
- New CSS goes in `docs/_sass/minima/custom-styles.scss` only if truly needed
- Keep parity with the homepage visual structure: card or list of items, meta row (date · source), optional badge

### 4. Landing page (`docs/<section>/index.md`)

```yaml
---
layout: <section>
title: "Section Title — eof.news"
description: "One-line description for SEO."
permalink: /<section>/
---
```

- Minimal frontmatter — the layout does all the work
- Permalink must match the nav link you'll add next

### 5. Header nav link (`docs/_includes/header.html`)

Add inside `.nav-items`:
```html
<a class="nav-item" href="/<section>/">Label</a>
```

Order matters — insert at a logical position relative to existing links.

### 6. GitHub Actions workflow (`.github/workflows/<section>.yml`)

Copy the structure from `dailynewspublisher.yml`. Key fields to set:
- `schedule` — cron for how often the section refreshes
- `run` — `python main.py --action=<section>`
- `name` — descriptive job name

---

## Common Mistakes

| Mistake | Fix |
|--------|-----|
| Creating a new layout that duplicates `base.html` scaffold | Always set `layout: base` in your layout's frontmatter |
| Writing inline CSS in the layout | Add to `custom-styles.scss` instead |
| New layout but no landing page | Both are required — the layout alone is unreachable |
| Forgetting `generated_at` in JSON | Include it; useful for debugging stale data |
| Permalink in landing page doesn't match nav link href | They must be identical |
| Adding the section to `main.py` but not to a workflow | Without a workflow, the data never refreshes |
| External Python deps | Stdlib + feedparser + bs4 + requests only |

---

## Quick Reference

| Layer | File path |
|-------|-----------|
| Generator | `<section>.py` |
| Data | `docs/_data/<section>.json` |
| Layout | `docs/_layouts/<section>.html` |
| Landing page | `docs/<section>/index.md` |
| Nav link | `docs/_includes/header.html` |
| Workflow | `.github/workflows/<section>.yml` |
| Global CSS | `docs/_sass/minima/custom-styles.scss` |
| main.py | `main.py` (add `case "<section>":`) |
