# Layout Consistency Design

**Date:** 2026-02-28
**Status:** Approved

## Goal

Establish a shared layout grammar across all tracker/section pages without destroying each page's unique personality.

## The 4 Rules

### Rule 1 — Page structure order
Every page follows: **stats bar → featured card → `##` section heading → list → footer**
Pages without a "featured" concept (Outages) skip the featured block.

### Rule 2 — Stats bar pills are uniform
Same pill style everywhere:
```html
padding:4px 12px; border-radius:12px; font-weight:bold;
```
- Pills that have anchors to link to stay as `<a>` (GitHub, Models, CVEs)
- Pills without anchor targets stay as `<span>` (Android, iOS)
- Outages gets a minimal stats bar: active incident count + timestamp

### Rule 3 — Card list items share a base style
```html
border:1px solid #e5e7eb; border-radius:8px; padding:0.85em;
```
- Android/iOS keep their colored left accent stripe (platform identity)
- Outages keeps its left-only border (alert/urgency semantics)
- Models "new releases" section (currently bottom-border only) gets normalized

### Rule 4 — Unified footer
Every page ends with:
```html
---
<p style="font-size:0.8em; color:#9ca3af;">Data from [Source] · Updated: [timestamp]</p>
```
- Android and iOS: add footer (currently missing entirely)
- Outages: add `---` before existing timestamp
- GitHub, Models, CVEs: already have this — verify/normalize wording

## What Is NOT Changed
- Platform colors: amber=GitHub, purple=Models, red=CVEs, green=Android, blue=iOS
- GitHub charts section
- CVE severity grouping structure
- Featured card names (Repo of the Day, Model of the Day, Top Threat, Latest)
- Outages left-border-only incident cards

## Files to Touch

| File | Changes |
|------|---------|
| `android.py` | Add `## Latest News` heading + footer in `_generate_page` |
| `ios.py` | Add `## Latest News` heading + footer in `_generate_page` |
| `outages.py` | Add minimal stats bar + `---` before timestamp in `_generate_page` |
| `docs/ai/models.md` | Normalize Models "new releases" card style (bottom-border → full border) |
| `docs/github/trending.md` | Verify footer wording |
| `docs/security/cves.md` | Verify footer wording / section heading presence |
