# Android Developer Section — Design

**Date:** 2026-02-28
**Status:** Approved

## Overview

Add a dedicated Android developer section at `/android/` following the same pattern as `/github/` and `/ai/models/`. The section surfaces both curated Android news (RSS) and trending Android GitHub repos in one place, updated daily via GitHub Actions.

## New Files

| File | Purpose |
|---|---|
| `android.py` | Fetches RSS feeds + GitHub Search API, generates data + page |
| `docs/_data/android.json` | Data consumed by the Jekyll page |
| `docs/android/index.md` | Rendered page at `/android/` |
| `.github/workflows/androidtracker.yml` | Daily automation |

**Modifications:**
- `main.py`: add `case "android"` → `from android import publish_android; publish_android()`
- `docs/_includes/header.html`: add nav link `/android/`

## RSS Sources

| Source | Feed URL |
|---|---|
| Android Developers Blog | `https://feeds.feedburner.com/blogspot/hsDu` |
| ProAndroidDev | `https://proandroiddev.com/feed` |
| Android Authority | `https://www.androidauthority.com/feed/` |
| Kotlin Blog | `https://blog.jetbrains.com/kotlin/feed/` |
| Android Weekly | `https://androidweekly.net/issues/rss` |

Top ~8 articles selected by recency + keyword relevance. Keywords: kotlin, jetpack compose, android studio, coroutines, flow, viewmodel, room, hilt, material design, gradle, apk, aab, play store, wear os, android tv.

## GitHub Data

Two GitHub Search queries:
1. `topic:android language:kotlin sort:stars per_page=20`
2. `topic:jetpack-compose sort:updated per_page=15`

~20 repos total after deduplication. Star delta tracking via `docs/_data/android_history.json` (same mechanism as `github_trending.py`). Badges: NEW (blue), RISING +N (green), COOLING (red).

**Repo of the Day:** same cooldown logic as GitHub tracker (30-day no-repeat, language rotation).

## Page Layout

```
[Stats chips: N repos · N articles · Top language · Most starred]

## 🤖 Repo of the Day
[Spotlight card with avatar, name, description, stars, language, delta]

## Latest Android News
[~8 article cards: title → external link, source name, date, excerpt]

## Trending Android Repos
[Repo cards with badges, stars, forks, language badge, topics, star delta]

---
[Data from GitHub Search API + RSS · Updated: <timestamp>]
```

## `docs/_data/android.json` Schema

```json
{
  "generated_at": "2026-02-28 10:00:00 UTC",
  "repos": [...],           // same shape as github.json repos
  "featured_repo": {...},   // Repo of the Day
  "top_language": "Kotlin",
  "articles": [
    {
      "title": "...",
      "url": "...",
      "source": "Android Developers Blog",
      "published": "2026-02-27T...",
      "excerpt": "..."
    }
  ]
}
```

## Workflow

```yaml
# .github/workflows/androidtracker.yml
schedule: cron '0 8 * * *'   # 08:00 UTC = 09:00 Rome
run: python main.py --action=android
```

## History File

`docs/_data/android_history.json` — same structure as `github_history.json`:
```json
{
  "snapshots": [
    { "date": "2026-02-28", "repos": { "owner/repo": 12345 } }
  ],
  "featured_history": ["owner/repo", ...]
}
```
