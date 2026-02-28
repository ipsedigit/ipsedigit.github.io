# eof.news Brand Identity Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the ipsedigit placeholder logo with a proper eof.news SVG mark and add a homepage hero banner.

**Architecture:** Create two SVG files (logo + favicon), update header and head includes to reference them, and rework the homepage to use `layout: base` with a custom dark hero section instead of the auto-generated `<h1>` from `layout: page`.

**Tech Stack:** SVG, Jekyll/Liquid, JetBrains Mono (already loaded globally)

---

### Task 1: Create the logo SVG

**Files:**
- Create: `docs/assets/images/logo.svg`

**Step 1: Create the file**

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40" width="40" height="40">
  <rect width="40" height="40" rx="6" fill="#111111"/>
  <text
    x="50%"
    y="50%"
    font-family="'JetBrains Mono', 'Courier New', monospace"
    font-size="13"
    font-weight="700"
    fill="#ffffff"
    text-anchor="middle"
    dominant-baseline="central"
    letter-spacing="-0.5"
  >eof</text>
</svg>
```

**Step 2: Verify**

Open the file in a browser. Should show a dark rounded square with white bold `eof` centered.

---

### Task 2: Create the favicon SVG

**Files:**
- Create: `docs/assets/images/favicon.svg`

**Step 1: Create the file**

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <rect width="32" height="32" rx="4" fill="#111111"/>
  <text
    x="50%"
    y="50%"
    font-family="'JetBrains Mono', 'Courier New', monospace"
    font-size="11"
    font-weight="700"
    fill="#ffffff"
    text-anchor="middle"
    dominant-baseline="central"
  >eof</text>
</svg>
```

**Step 2: Verify**

Open in browser — should look identical to logo but at 32×32.

---

### Task 3: Update header to use logo.svg

**Files:**
- Modify: `docs/_includes/header.html`

**Step 1: Replace the img src**

Find:
```html
<img class="site-logo" src="/assets/images/logo.png" alt="{{ site.title | escape }}" width="28" height="28" />
```

Replace with:
```html
<img class="site-logo" src="/assets/images/logo.svg" alt="{{ site.title | escape }}" width="28" height="28" />
```

---

### Task 4: Update favicon reference in head.html

**Files:**
- Modify: `docs/_includes/head.html`

**Step 1: Replace the favicon link**

Find:
```html
<link rel="icon" href="{{ '/assets/images/favicon.png' | relative_url }}" type="image/png">
```

Replace with:
```html
<link rel="icon" href="{{ '/assets/images/favicon.svg' | relative_url }}" type="image/svg+xml">
```

---

### Task 5: Rework homepage — layout + hero banner

**Files:**
- Modify: `docs/index.html` — front matter + add hero section

**Step 1: Update front matter**

Replace:
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

With:
```yaml
---
layout: base
title: "eof.news — Today's tech signal for engineers who build"
description: "Daily curated tech signal: AI, security, cloud, devtools. For engineers who build. No noise."
keywords: "tech news, AI news, security news, cloud computing, developer tools, software engineering, devops, kubernetes, programming, trending tech"
---
```

**Step 2: Add hero banner as the first element after the `</style>` block**

The `</style>` block ends at the closing tag before the ad/post content. Insert the following immediately after `</style>` and before the first Liquid tag:

```html
<div style="background:#111; margin: -1.5rem -1rem 2rem -1rem; padding: 2.5rem 1rem; text-align:center;">
  <div style="font-family:'JetBrains Mono', monospace; font-size:2rem; font-weight:700; letter-spacing:0.02em; line-height:1;">
    <span style="color:#fff;">eof</span><span style="color:#555;">.news</span>
  </div>
</div>
```

> Note on the negative margins: the `.wrapper` in `layout: base` has horizontal padding. The negative margins bleed the dark band to the full wrapper width. Adjust if the site wrapper padding differs.

**Step 3: Verify**

Load the homepage. Confirm:
- Dark band appears at top, full width of content area
- `eof` in white, `.news` in muted gray
- No `<h1>` title rendered (layout is now `base`, not `page`)
- Featured article card appears immediately below the hero

---

> **Note:** No automated tests — this is a template/SVG change. All verification is visual in the browser.
