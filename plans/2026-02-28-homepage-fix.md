# Homepage Fix Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the homepage consistent with iOS/Android/Devs pages by adding a page header with badge and a featured hero card.

**Architecture:** Single-file change to `docs/index.html`. Switch from `layout: base` to `layout: page` (renders title + badge), add a hero card using the first post from `paginator.posts`, then move the top ad below the hero so content shows first.

**Tech Stack:** Jekyll/Liquid, GitHub Pages, Minima theme

---

### Task 1: Update front matter

**Files:**
- Modify: `docs/index.html` lines 1-6

**Step 1: Change layout and add badge metadata**

Replace the current front matter:
```yaml
---
layout: base
title: "eof.news — Today's tech signal for engineers who build"
description: "Daily curated tech signal: AI, security, cloud, devtools. For engineers who build. No noise."
keywords: "tech news, AI news, security news, cloud computing, developer tools, software engineering, devops, kubernetes, programming, trending tech"
---
```

With:
```yaml
---
layout: page
title: "eof.news — Today's tech signal for engineers who build"
description: "Daily curated tech signal: AI, security, cloud, devtools. For engineers who build. No noise."
keywords: "tech news, AI news, security news, cloud computing, developer tools, software engineering, devops, kubernetes, programming, trending tech"
title_badge: "📰 Latest"
title_badge_bg: "#f0f9ff"
title_badge_color: "#0284c7"
---
```

**Step 2: Verify**

The `docs/_layouts/page.html` wraps content in `<article class="post">` with `<h1>` showing the title + badge. This is the same pattern used by iOS, Android, and Devs pages.

---

### Task 2: Add hero card and reorder content

**Files:**
- Modify: `docs/index.html` — replace everything after the `<style>` block

**Step 1: Replace the content section**

Find this block (lines 145–219, everything after `</style>`):
```liquid
<div class="ad-space" id="ad-top">
  {% if site.adsense_id %}
  ...
  {% endif %}
</div>

{% assign post_count = 0 %}
{% for post in paginator.posts %}
...
{% endfor %}

{% if paginator.total_pages > 1 %}
...
{% endif %}

<div class="ad-space" id="ad-bottom">
...
</div>
```

Replace with:

```liquid
{% assign featured = paginator.posts | first %}
{% if featured %}
<div style="margin-bottom:2em; padding:1.25em; border:2px solid #0284c7; border-radius:8px; background:#f0f9ff;">
  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap; margin-bottom:0.6em;">
    <span style="padding:3px 10px; border-radius:12px; font-size:0.78em; font-weight:bold; background:#0284c7; color:#fff;">&#9733; Latest</span>
    <span style="font-size:0.78em; color:#6b7280;">
      {% if featured.source %}{{ featured.source }} &middot; {% endif %}
      {{ featured.date | date: "%b %d, %Y" }}
      {% if featured.niche_category %}
        &middot; <a href="/niche/{{ featured.niche_category }}/" class="niche-badge niche-badge--{{ featured.niche_category }}">{{ featured.niche_category }}</a>
      {% endif %}
    </span>
  </div>
  <div style="font-weight:700; font-size:1.1em; margin-bottom:0.4em;">
    {% if featured.external_url %}
    <a href="{{ featured.external_url }}" target="_blank" rel="noopener" style="color:#0284c7; text-decoration:none;">{{ featured.title }}</a>
    {% else %}
    <a href="{{ featured.url | relative_url }}" style="color:#0284c7; text-decoration:none;">{{ featured.title }}</a>
    {% endif %}
  </div>
  {% if featured.description %}
  <p style="margin:0; font-size:0.88em; color:#374151; line-height:1.5;">{{ featured.description | truncate: 200 }}</p>
  {% endif %}
</div>
{% endif %}

<div class="ad-space" id="ad-top">
  {% if site.adsense_id %}
  <ins class="adsbygoogle" style="display:block" data-ad-client="{{ site.adsense_id }}" data-ad-slot="TOP" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  {% endif %}
</div>

{% assign post_count = 0 %}
{% for post in paginator.posts offset:1 %}
{% assign post_count = post_count | plus: 1 %}

<article class="post-item">
  <h2 class="post-title">
    {% if post.external_url %}
    <a href="{{ post.external_url }}" target="_blank" rel="noopener">{{ post.title }}</a>
    {% else %}
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    {% endif %}
  </h2>
  <div class="post-meta">
    {{ post.date | date: "%b %d, %Y" }}
    {% if post.source %} · {{ post.source }}{% endif %}
    {% if post.niche_category %}
      · <a href="/niche/{{ post.niche_category }}/" class="niche-badge niche-badge--{{ post.niche_category }}">{{ post.niche_category }}</a>
    {% endif %}
    {% if post.categories.size > 0 %}
    · <span class="post-tags">
      {% for category in post.categories %}
      {% assign tag_slug = category | slugify: "latin" %}
      <a href="/tags/{{ tag_slug }}/">{{ category }}</a>
      {% endfor %}
    </span>
    {% endif %}
  </div>
  {% if post.description %}
  <p class="post-preview">{{ post.description | truncate: 160 }}</p>
  {% endif %}
  {% if post.image %}
  <div class="post-image">
    <img src="{{ post.image }}" alt="" loading="lazy">
  </div>
  {% endif %}
</article>

{% assign mod = post_count | modulo: 8 %}
{% if mod == 0 %}
<div class="ad-space">
  {% if site.adsense_id %}
  <ins class="adsbygoogle" style="display:block" data-ad-client="{{ site.adsense_id }}" data-ad-slot="MID" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  {% endif %}
</div>
{% endif %}

{% endfor %}

{% if paginator.total_pages > 1 %}
<nav class="pagination">
  {% if paginator.previous_page %}
    <a href="{{ paginator.previous_page_path | relative_url }}">&#8592; Newer</a>
  {% endif %}
  <span class="current-page">Page {{ paginator.page }} of {{ paginator.total_pages }}</span>
  {% if paginator.next_page %}
    <a href="{{ paginator.next_page_path | relative_url }}">Older &#8594;</a>
  {% endif %}
</nav>
{% endif %}

<div class="ad-space" id="ad-bottom">
  {% if site.adsense_id %}
  <ins class="adsbygoogle" style="display:block" data-ad-client="{{ site.adsense_id }}" data-ad-slot="BOTTOM" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  {% endif %}
</div>
```

**Step 2: Verify the key changes**

- Hero card appears before the ad
- Article loop uses `offset:1` (skips the hero post)
- `post_count` resets to 0 for the offset loop — mid-ad fires every 8 articles in the list
- Pagination and bottom ad unchanged

---

### Task 3: Manual verification

**Step 1: Build locally (if Jekyll is available)**
```bash
cd docs && bundle exec jekyll serve --incremental
```
Open `http://localhost:4000` and confirm:
- Page title `eof.news — Today's tech signal for engineers who build` renders with badge `📰 Latest`
- Hero card shows in blue border before the ad
- Article list starts with the second post

**Step 2: If no local Jekyll, push and check GitHub Pages**
Commit and push, wait ~30s, verify at `https://ipsedigit.github.io`.

---

> **Note:** No tests to write — this is a Liquid template change. Verification is visual.
