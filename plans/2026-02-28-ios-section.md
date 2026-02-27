# iOS Developer Section Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a dedicated `/ios/` tracker page and `ios` niche to the eof.news pipeline, serving iOS developers with curated Apple platform, Swift, and community content.

**Architecture:** New `ios.py` script fetches 6 Apple/iOS RSS feeds, generates `docs/_data/ios.json` and `docs/ios/index.md` (static page with spotlight + sections). Separately, `ios` is added as a 6th niche in `const.py` so daily news articles about Swift/Xcode/UIKit flow through the existing two-pass selector.

**Tech Stack:** Python stdlib + feedparser (already in requirements), Jekyll/Liquid for the page, GitHub Actions for the workflow.

---

### Task 1: Add iOS niche + keywords to `const.py`

**Files:**
- Modify: `const.py`

**Step 1: Add iOS to CONTENT_CATEGORIES**

In `const.py`, after the `'software-engineering'` entry in `CONTENT_CATEGORIES` (around line 51), add:

```python
    'ios': ['swift', 'swiftui', 'uikit', 'appkit', 'xcode', 'wwdc', 'ios', 'ipados',
            'macos', 'watchos', 'tvos', 'visionos', 'app store', 'testflight',
            'core data', 'combine', 'swift package manager', 'spm', 'objective-c',
            'apple developer', 'app clip', 'widget kit', 'live activity'],
```

**Step 2: Add iOS to NICHE_CATEGORIES**

Change line 59:
```python
NICHE_CATEGORIES = ['ai', 'software-engineering', 'devtools', 'cloud', 'security']
```
to:
```python
NICHE_CATEGORIES = ['ai', 'software-engineering', 'devtools', 'cloud', 'security', 'ios']
```

**Step 3: Add IOS_SUBNICHES dict**

After `SE_SUBNICHES` (after line 128), add:

```python
IOS_SUBNICHES = {
    'swift': ['swift', 'swiftui', 'swift package manager', 'spm', 'combine', 'async await',
              'swift concurrency', 'swift macros', 'swift evolution'],
    'xcode': ['xcode', 'instruments', 'simulator', 'xctest', 'xctestplan', 'xcframework',
              'build system', 'swift compiler'],
    'appstore': ['app store', 'testflight', 'app review', 'app store connect', 'in-app purchase',
                 'subscription', 'app store optimization', 'aso', 'rating', 'indie app'],
    'apple-platform': ['uikit', 'appkit', 'swiftui', 'wwdc', 'visionos', 'watchos', 'tvos',
                       'core data', 'cloudkit', 'push notification', 'widget', 'live activity',
                       'app clip', 'metal', 'arkit', 'core ml', 'vision framework'],
    'ios-release': ['ios 18', 'ios 19', 'xcode 16', 'xcode 17', 'swift 6', 'swift 7',
                    'macos sequoia', 'macos tahoe', 'ipados', 'release notes', 'beta'],
}
```

**Step 4: Register in NICHE_SUBNICHES**

Change the `NICHE_SUBNICHES` dict (around line 130):
```python
NICHE_SUBNICHES = {
    'ai': AI_SUBNICHES,
    'security': SECURITY_SUBNICHES,
    'cloud': CLOUD_SUBNICHES,
    'devtools': DEVTOOLS_SUBNICHES,
    'software-engineering': SE_SUBNICHES,
    'ios': IOS_SUBNICHES,
}
```

**Step 5: Add iOS-specific TITLE_BONUS entries**

In `TITLE_BONUS` (around line 598), add after the last entry:
```python
    r'(swift|swiftui|xcode|wwdc|uikit)': 25,              # iOS/Apple signal
```

**Step 6: Add iOS community blog sources to NEWS_SOURCES**

At the end of `NEWS_SOURCES`, before the closing `}`, add a new tier:

```python
    # --- TIER 10: iOS & Apple Ecosystem ---
    'nshipster': {
        'name': 'NSHipster',
        'feed_url': 'https://nshipster.com/feed.xml',
        'min_score': 0,
        'type': 'ios_blog',
        'score_boost': 35,
    },
    'hackingwithswift': {
        'name': 'Hacking with Swift',
        'feed_url': 'https://www.hackingwithswift.com/articles/rss',
        'min_score': 0,
        'type': 'ios_blog',
        'score_boost': 35,
    },
    'swiftbysundell': {
        'name': 'Swift by Sundell',
        'feed_url': 'https://swiftbysundell.com/feed.rss',
        'min_score': 0,
        'type': 'ios_blog',
        'score_boost': 35,
    },
```

**Step 7: Verify existing tests still pass**

```bash
cd C:\repo\ipsedigit.github.io
python -m pytest tests/ -v
```

Expected: all existing tests PASS (no test hardcodes the exact list of niches in NICHE_CATEGORIES).

**Step 8: Commit**

```bash
git add const.py
git commit -m "feat(ios): add ios niche, subniches, keywords, and ios_blog sources to const.py"
```

---

### Task 2: Create `ios.py` — the dedicated iOS tracker

**Files:**
- Create: `ios.py`

This script mirrors the pattern of `outages.py` and `models.py`. It fetches RSS feeds, builds a JSON data file, and generates a Jekyll page.

**Step 1: Write the file**

Create `ios.py` with the following content:

```python
"""
iOS Developer Tracker.
Fetches Apple Developer, Swift Blog, and iOS community RSS feeds.
Generates docs/_data/ios.json and docs/ios/index.md.
"""
import json
import os
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

import feedparser

DATA_DIR = "docs/_data"
OUTPUT_JSON = os.path.join(DATA_DIR, "ios.json")
OUTPUT_DIR = "docs/ios"
OUTPUT_PAGE = os.path.join(OUTPUT_DIR, "index.md")

MAX_ITEMS_PER_FEED = 8
MAX_AGE_DAYS = 90

FEEDS = [
    {
        "key": "swift_blog",
        "name": "Swift Blog",
        "url": "https://www.swift.org/atom.xml",
        "section": "apple_official",
        "is_spotlight_candidate": True,
    },
    {
        "key": "apple_dev",
        "name": "Apple Developer News",
        "url": "https://developer.apple.com/news/rss/news.rss",
        "section": "apple_official",
        "is_spotlight_candidate": True,
    },
    {
        "key": "nshipster",
        "name": "NSHipster",
        "url": "https://nshipster.com/feed.xml",
        "section": "community",
        "is_spotlight_candidate": False,
    },
    {
        "key": "hackingwithswift",
        "name": "Hacking with Swift",
        "url": "https://www.hackingwithswift.com/articles/rss",
        "section": "community",
        "is_spotlight_candidate": False,
    },
    {
        "key": "swiftbysundell",
        "name": "Swift by Sundell",
        "url": "https://swiftbysundell.com/feed.rss",
        "section": "community",
        "is_spotlight_candidate": False,
    },
    {
        "key": "iosdevweekly",
        "name": "iOS Dev Weekly",
        "url": "https://iosdevweekly.com/issues.rss",
        "section": "community",
        "is_spotlight_candidate": False,
    },
]

SPOTLIGHT_KEYWORDS = [
    'swift 6', 'swift 7', 'swift 8',
    'xcode 16', 'xcode 17', 'xcode 18',
    'ios 18', 'ios 19', 'ios 20',
    'wwdc',
    'swiftui',
]


def _fetch_feed(feed_config):
    """Fetch and parse an RSS feed. Returns list of normalized items."""
    name = feed_config["name"]
    url = feed_config["url"]
    print(f"  Fetching {name}...")
    try:
        parsed = feedparser.parse(url)
        items = []
        cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)
        for entry in parsed.entries[:MAX_ITEMS_PER_FEED]:
            pub = _parse_date(entry)
            if pub and pub < cutoff:
                continue
            items.append({
                "title": entry.get("title", "").strip(),
                "url": entry.get("link", ""),
                "published": pub.isoformat() if pub else "",
                "summary": _clean_summary(entry.get("summary", "")),
                "source": name,
                "source_key": feed_config["key"],
            })
        print(f"    {len(items)} items")
        return items
    except Exception as e:
        print(f"    Error: {e}")
        return []


def _parse_date(entry):
    """Parse published date from feedparser entry. Returns datetime or None."""
    for attr in ("published_parsed", "updated_parsed"):
        val = getattr(entry, attr, None)
        if val:
            try:
                import time as _time
                return datetime.fromtimestamp(_time.mktime(val), tz=timezone.utc)
            except Exception:
                pass
    return None


def _clean_summary(text):
    """Strip HTML tags and truncate summary."""
    import re
    text = re.sub(r"<[^>]+>", "", text)
    text = text.strip()
    return text[:200] + "…" if len(text) > 200 else text


def _pick_spotlight(items):
    """Pick the most relevant item as spotlight from apple_official items.

    Prefers items whose title contains a SPOTLIGHT_KEYWORDS match.
    Falls back to most recent item.
    """
    if not items:
        return None
    title_lower = lambda i: i["title"].lower()
    for kw in SPOTLIGHT_KEYWORDS:
        for item in items:
            if kw in title_lower(item):
                return item
    return items[0]


def _format_date(iso_str):
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%b %d, %Y")
    except (ValueError, AttributeError):
        return iso_str[:10]


def _generate_page(data):
    """Generate Jekyll markdown page for /ios/."""
    spotlight = data.get("spotlight")
    official = data.get("apple_official", [])
    community = data.get("community", [])
    generated_at = data.get("generated_at", "")

    lines = [
        "---",
        "layout: page",
        'title: "iOS Developer"',
        'description: "Curated news and resources for iOS developers. Swift, SwiftUI, Xcode, WWDC, App Store, and the Apple dev community."',
        "permalink: /ios/",
        "---",
        "",
    ]

    # Spotlight card
    if spotlight:
        pub_str = _format_date(spotlight.get("published", ""))
        lines += [
            '## Spotlight',
            '',
            f'<div style="margin-bottom:1.5em; padding:1em; border:2px solid #0071e3; border-radius:12px; background:#f0f7ff;">',
            f'  <div style="display:flex; align-items:center; gap:0.5em; margin-bottom:0.5em; flex-wrap:wrap;">',
            f'    <span style="padding:2px 10px; border-radius:12px; font-size:0.8em; background:#0071e3; color:#fff; font-weight:bold;">&#9733; Apple</span>',
            f'    <span style="font-size:0.82em; color:#6b7280;">{spotlight["source"]}</span>',
            f'    {"<span style=\"font-size:0.82em; color:#6b7280;\">" + pub_str + "</span>" if pub_str else ""}',
            f'  </div>',
            f'  <div style="font-weight:700; font-size:1.1em; margin-bottom:0.4em;">',
            f'    <a href="{spotlight["url"]}" target="_blank" rel="noopener" style="color:#0071e3; text-decoration:none;">{spotlight["title"]}</a>',
            f'  </div>',
            f'  {"<p style=\"margin:0; color:#374151; font-size:0.9em;\">" + spotlight["summary"] + "</p>" if spotlight.get("summary") else ""}',
            f'</div>',
            '',
        ]

    # Apple Official section
    if official:
        non_spotlight = [i for i in official if not spotlight or i["url"] != spotlight["url"]]
        if non_spotlight:
            lines += ['## Apple Official', '']
            for item in non_spotlight[:6]:
                pub_str = _format_date(item.get("published", ""))
                date_part = f' <span style="font-size:0.8em; color:#9ca3af;">— {pub_str}</span>' if pub_str else ''
                lines.append(
                    f'- **[{item["title"]}]({item["url"]})**{date_part}  '
                    f'<span style="font-size:0.78em; color:#6b7280;">{item["source"]}</span>'
                )
            lines.append('')

    # Community section
    if community:
        lines += ['## Community', '']
        for item in community[:12]:
            pub_str = _format_date(item.get("published", ""))
            date_part = f' <span style="font-size:0.8em; color:#9ca3af;">— {pub_str}</span>' if pub_str else ''
            lines.append(
                f'- **[{item["title"]}]({item["url"]})**{date_part}  '
                f'<span style="font-size:0.78em; color:#6b7280;">{item["source"]}</span>'
            )
        lines.append('')

    lines += [
        '---',
        '',
        f'<p style="font-size:0.8em; color:#9ca3af;">Updated: {generated_at}</p>',
        '',
    ]

    return '\n'.join(lines)


def publish_ios():
    """Main entry point."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Fetching iOS feeds...")
    all_items = []
    for feed_config in FEEDS:
        items = _fetch_feed(feed_config)
        for item in items:
            item["section"] = feed_config["section"]
            item["is_spotlight_candidate"] = feed_config["is_spotlight_candidate"]
        all_items.extend(items)

    # Sort by date desc
    all_items.sort(key=lambda i: i.get("published", ""), reverse=True)

    official_items = [i for i in all_items if i["section"] == "apple_official"]
    community_items = [i for i in all_items if i["section"] == "community"]
    spotlight_candidates = [i for i in all_items if i["is_spotlight_candidate"]]
    spotlight = _pick_spotlight(spotlight_candidates)

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    data = {
        "generated_at": now_str,
        "spotlight": spotlight,
        "apple_official": official_items,
        "community": community_items,
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  JSON written: {OUTPUT_JSON}")

    page = _generate_page(data)
    with open(OUTPUT_PAGE, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"  Page written: {OUTPUT_PAGE}")
```

**Step 2: Run it manually to verify it works**

```bash
cd C:\repo\ipsedigit.github.io
python ios.py
```

Wait — `ios.py` defines functions but the entry point is `publish_ios()`. Run via:

```bash
python -c "from ios import publish_ios; publish_ios()"
```

Expected output:
```
Fetching iOS feeds...
  Fetching Swift Blog...
    N items
  Fetching Apple Developer News...
    N items
  ...
  JSON written: docs/_data/ios.json
  Page written: docs/ios/index.md
```

Check that `docs/_data/ios.json` and `docs/ios/index.md` exist and look reasonable.

**Step 3: Write a smoke test**

Create `tests/test_ios.py`:

```python
import json
import os
import sys
from unittest.mock import patch, MagicMock
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from ios import _pick_spotlight, _clean_summary, _format_date, _generate_page


def _item(title, url="http://example.com", published="2026-01-01T00:00:00+00:00", source="Swift Blog"):
    return {"title": title, "url": url, "published": published, "summary": "Test summary.", "source": source, "source_key": "test"}


def test_pick_spotlight_prefers_keyword_match():
    items = [
        _item("Random article"),
        _item("Swift 6 is here"),
        _item("Another article"),
    ]
    result = _pick_spotlight(items)
    assert result["title"] == "Swift 6 is here"


def test_pick_spotlight_falls_back_to_first():
    items = [_item("No keywords here"), _item("Also nothing")]
    result = _pick_spotlight(items)
    assert result == items[0]


def test_pick_spotlight_empty():
    assert _pick_spotlight([]) is None


def test_clean_summary_strips_html():
    result = _clean_summary("<p>Hello <b>world</b></p>")
    assert "<" not in result
    assert "Hello world" in result


def test_clean_summary_truncates():
    long_text = "x" * 300
    result = _clean_summary(long_text)
    assert len(result) <= 203  # 200 + "…"
    assert result.endswith("…")


def test_format_date_parses_iso():
    result = _format_date("2026-01-15T10:00:00+00:00")
    assert "Jan" in result
    assert "2026" in result


def test_format_date_empty():
    assert _format_date("") == ""


def test_generate_page_contains_permalink():
    data = {
        "generated_at": "2026-01-01 00:00:00 UTC",
        "spotlight": _item("Swift 6 released"),
        "apple_official": [_item("News item 1"), _item("News item 2")],
        "community": [_item("Community post", source="NSHipster")],
    }
    page = _generate_page(data)
    assert "permalink: /ios/" in page
    assert "Swift 6 released" in page
    assert "Community" in page


def test_generate_page_no_spotlight():
    data = {
        "generated_at": "2026-01-01 00:00:00 UTC",
        "spotlight": None,
        "apple_official": [],
        "community": [],
    }
    page = _generate_page(data)
    assert "permalink: /ios/" in page
```

**Step 4: Run the tests**

```bash
python -m pytest tests/test_ios.py -v
```

Expected: all tests PASS.

**Step 5: Commit**

```bash
git add ios.py tests/test_ios.py docs/_data/ios.json docs/ios/index.md
git commit -m "feat(ios): add ios.py tracker and initial ios/ page"
```

---

### Task 3: Wire iOS into `main.py` and `header.html`

**Files:**
- Modify: `main.py`
- Modify: `docs/_includes/header.html`

**Step 1: Add ios case to main.py**

In `main.py`, after the `case "outages":` block (line 22), add:

```python
        case "ios":
            from ios import publish_ios
            publish_ios()
```

Also update the help string on line 34:
```python
    parser.add_argument("--action", type=str, default="news", help="Action: news, digest, cves, models, github, bootleg, outages, ios")
```

**Step 2: Add iOS nav link to header.html**

In `docs/_includes/header.html`, after the `<a class="nav-item" href="/outages/">Outages</a>` line (line 23), add:

```html
        <a class="nav-item" href="/ios/">iOS</a>
```

**Step 3: Verify main.py dispatch works**

```bash
python main.py --action=ios
```

Expected: same output as running `publish_ios()` directly (feeds fetched, files written).

**Step 4: Commit**

```bash
git add main.py docs/_includes/header.html
git commit -m "feat(ios): wire ios action in main.py and add iOS nav link"
```

---

### Task 4: Create GitHub Actions workflow

**Files:**
- Create: `.github/workflows/iostracker.yml`

**Step 1: Write the workflow file**

```yaml
name: iOS Tracker

on:
  schedule:
    - cron: '0 8 * * *'   # 08:00 UTC daily (09:00 Rome)
  workflow_dispatch:

jobs:
  track-ios:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout main branch
      uses: actions/checkout@v4
      with:
        ref: main

    - name: Configure Git
      run: |
        git config user.name "github-actions[bot]"
        git config user.email "github-actions[bot]@users.noreply.github.com"

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run iOS tracker
      run: python main.py --action=ios

    - name: Commit and Push changes
      run: |
        find . -type d -name "__pycache__" -exec rm -r {} +
        find . -name "*.pyc" -delete
        git add .
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
        git commit -m "Auto: ios update at ${TIMESTAMP}" || echo "No changes to commit"
        git push origin main
```

**Step 2: Verify the workflow file is valid YAML**

```bash
python -c "import yaml; yaml.safe_load(open('.github/workflows/iostracker.yml'))"
```

Expected: no output (no errors).

**Step 3: Commit**

```bash
git add .github/workflows/iostracker.yml
git commit -m "feat(ios): add iostracker GitHub Actions workflow"
```

---

### Task 5: Full run + final check

**Step 1: Run all tests**

```bash
python -m pytest tests/ -v
```

Expected: all tests PASS including the new `test_ios.py`.

**Step 2: Verify Jekyll build doesn't break**

Check that `docs/ios/index.md` has valid frontmatter:

```bash
python -c "
with open('docs/ios/index.md') as f:
    content = f.read()
assert content.startswith('---'), 'Missing frontmatter'
assert 'permalink: /ios/' in content, 'Missing permalink'
print('OK')
"
```

Expected: `OK`

**Step 3: Spot-check ios.json structure**

```bash
python -c "
import json
data = json.load(open('docs/_data/ios.json'))
assert 'spotlight' in data
assert 'apple_official' in data
assert 'community' in data
assert 'generated_at' in data
print('Keys OK')
print('Spotlight:', data['spotlight']['title'] if data['spotlight'] else 'None')
print('Official items:', len(data['apple_official']))
print('Community items:', len(data['community']))
"
```

**Step 4: Final commit if any cleanup needed**

```bash
git add -p   # review any remaining changes
git commit -m "feat(ios): finalize ios section"
```
