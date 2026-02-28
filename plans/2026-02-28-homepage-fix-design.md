# Homepage Fix Design
Date: 2026-02-28

## Problem
The homepage (`docs/index.html`) is inconsistent with the iOS, Android, and Devs pages:
- Uses `layout: base` instead of `layout: page` — no title/header rendered
- No featured hero card at the top
- Top ad appears before any content

## Goal
Align the homepage with the iOS/Android/Devs pattern:
- Page title with badge
- Featured "★ Latest" hero card (first post)
- Ad below the hero, not at the very top

## Front Matter Changes
```yaml
layout: page   # was: base
title_badge: "📰 Latest"
title_badge_bg: "#f0f9ff"
title_badge_color: "#0284c7"
```

## New Page Structure
1. **Hero card** — `paginator.posts | first`
   - Border: `2px solid #0284c7`, background `#f0f9ff`
   - `★ Latest` badge (purple pill, same as other pages)
   - Title linked to `external_url` (target _blank) or `post.url`
   - Meta: date · source · niche badge
   - Description preview (truncated to 200 chars)
2. **Top ad** — moved below hero
3. **Article list** — `paginator.posts offset:1` using existing `.post-item` cards
4. **Mid-list ads** — every 8 posts (counter must account for offset)
5. **Pagination** — unchanged

## Files Changed
- `docs/index.html` — only file to change

## Out of Scope
- Card style changes (keep `.post-item`)
- Niche grouping
- Nav changes
