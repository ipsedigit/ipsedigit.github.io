# Developer Profiles Design

**Date:** 2026-02-25
**Goal:** Give featured indie developers permanent profile pages on eof.news (`/devs/<slug>/`) to incentivize genuine backlinks.

## Problem

Current `/creators/` page is a generic list — no one links to "a list I'm on." Individual profile pages give devs something personal to reference from their About page or blog sidebar, creating natural dofollow backlink exchange.

## Design

### Data: `FEATURED_DEVS` in `const.py`

```python
'juliaevans': {
    'name': 'Julia Evans',
    'slug': 'julia-evans',
    'url': 'https://jvns.ca',
    'bio': 'Writes about Linux, networking, and debugging in a way that makes complex topics approachable.',
    'avatar': '',  # optional URL
    'source_name': 'Julia Evans',  # must match NEWS_SOURCES[key]['name']
    'featured_since': '2026-02-25',
}
```

Initial set: all 7 existing creators from `NEWS_SOURCES` with `type: 'creator'`.

### Generation: `generate_dev_profiles()` in `news.py`

Called during `publish_news()`. For each dev in `FEATURED_DEVS`:
1. Writes `docs/_data/devs.json` (directory data)
2. Writes `docs/devs/<slug>.md` (individual profile page)

Profile page frontmatter:
```yaml
layout: dev
title: "Julia Evans — eof.news Developer Profile"
description: "..."
permalink: /devs/julia-evans/
dev_name: Julia Evans
dev_url: https://jvns.ca
dev_bio: "..."
dev_avatar: ""
dev_source_name: Julia Evans
dev_featured_since: "2026-02-25"
```

The layout (`docs/_layouts/dev.html`) renders:
- Name, bio, avatar (if provided)
- Dofollow link to their blog
- "Featured on eof.news since [date]"
- Auto-populated list of their curated posts (matched by `post.source == dev_source_name`)

### Pages

- `/devs/` — Directory: grid of dev cards linking to individual profiles
- `/devs/<slug>/` — Individual profile page

### Nav

Add "Devs" link to `docs/_includes/header.html`.

### Files to modify/create

| File | Action |
|---|---|
| `const.py` | Add `FEATURED_DEVS` dict |
| `news.py` | Add `generate_dev_profiles()`, call from `publish_news()` |
| `docs/_layouts/dev.html` | New layout for profile pages |
| `docs/devs/index.md` | New directory page |
| `docs/_includes/header.html` | Add "Devs" nav link |
| `main.py` | No change (news action already calls publish_news) |

### Backlink mechanism

1. Pipeline generates profile page
2. You email the dev: "We created a profile for you on eof.news: [link]"
3. They add it to their About/Featured section
4. Dofollow links flow both ways
