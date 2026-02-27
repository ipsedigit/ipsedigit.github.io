# Android Developer Section Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a dedicated `/android/` page that surfaces curated Android news (from RSS feeds) and trending Android GitHub repositories, updated daily via GitHub Actions.

**Architecture:** A new standalone `android.py` script mirrors the `github_trending.py` pattern exactly — it fetches RSS articles + GitHub Search API repos, computes star deltas via a history file, picks a Repo of the Day, and generates `docs/_data/android.json` + `docs/android/index.md`. A new GitHub Actions workflow runs it daily.

**Tech Stack:** Python 3 stdlib + feedparser (already in requirements.txt), GitHub Search API (no extra auth needed), Jekyll/Liquid for the page.

---

### Task 1: Create `android.py` — constants, RSS fetching, and GitHub search

**Files:**
- Create: `android.py`

**Context:** Look at `github_trending.py` lines 1–97 for the exact pattern of imports, constants, and `_github_search()`. Look at `news.py` lines 39–78 for the `feedparser` RSS pattern.

**Step 1: Create `android.py` with constants and RSS fetching**

```python
"""
Android Developer Tracker.
Fetches trending Android repos from GitHub Search API and
curated news from Android RSS feeds.
Generates docs/_data/android.json and docs/android/index.md.
"""
import json
import os
import re
import urllib.request
import urllib.error
import urllib.parse
import feedparser
from datetime import datetime, timezone, timedelta
from collections import Counter

DATA_DIR = "docs/_data"
OUTPUT_JSON = os.path.join(DATA_DIR, "android.json")
OUTPUT_DIR = "docs/android"
OUTPUT_PAGE = os.path.join(OUTPUT_DIR, "index.md")
HISTORY_JSON = os.path.join(DATA_DIR, "android_history.json")
STAR_DELTA_RISING_THRESHOLD = 30
FEATURED_COOLDOWN_DAYS = 30
MAX_ARTICLES = 10

GH_SEARCH_URL = "https://api.github.com/search/repositories"

RSS_SOURCES = [
    {"name": "Android Developers Blog", "url": "https://feeds.feedburner.com/blogspot/hsDu"},
    {"name": "ProAndroidDev",            "url": "https://proandroiddev.com/feed"},
    {"name": "Android Authority",        "url": "https://www.androidauthority.com/feed/"},
    {"name": "Kotlin Blog",              "url": "https://blog.jetbrains.com/kotlin/feed/"},
    {"name": "Android Weekly",           "url": "https://androidweekly.net/issues/rss"},
]

ANDROID_KEYWORDS = [
    "kotlin", "jetpack", "compose", "android studio", "coroutines",
    "viewmodel", "room", "hilt", "material", "gradle", "apk", "aab",
    "play store", "wear os", "android tv", "fragment", "retrofit",
    "architecture", "flow", "lifecycle", "navigation component",
]

LANGUAGE_COLORS = {
    "Kotlin": "#A97BFF",
    "Java":   "#b07219",
    "C++":    "#f34b7d",
    "C":      "#555555",
    "Python": "#3572A5",
    "Dart":   "#00B4AB",
}


def _fetch_rss_articles():
    """Fetch and score articles from Android RSS feeds. Returns list sorted by date."""
    articles = []
    for source in RSS_SOURCES:
        try:
            feed = feedparser.parse(source["url"])
            for entry in feed.entries[:15]:
                title = (entry.get("title") or "").strip()
                link = (entry.get("link") or "").strip()
                if not title or not link:
                    continue
                summary = (entry.get("summary") or entry.get("description") or "").strip()
                if summary:
                    summary = re.sub(r"<[^>]+>", "", summary).strip()[:200]
                # Parse date
                pub = entry.get("published_parsed") or entry.get("updated_parsed")
                if pub and len(pub) >= 6:
                    try:
                        dt = datetime(pub[0], pub[1], pub[2], pub[3], pub[4], pub[5], tzinfo=timezone.utc)
                    except (TypeError, ValueError):
                        dt = datetime.now(timezone.utc)
                else:
                    dt = datetime.now(timezone.utc)
                articles.append({
                    "title": title,
                    "url": link,
                    "source": source["name"],
                    "published": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "excerpt": summary,
                })
        except Exception as e:
            print(f"  RSS error [{source['name']}]: {e}")

    # Sort by date descending, deduplicate by URL
    seen_urls = set()
    unique = []
    articles.sort(key=lambda a: a["published"], reverse=True)
    for a in articles:
        if a["url"] not in seen_urls:
            seen_urls.add(a["url"])
            unique.append(a)

    print(f"  Articles fetched: {len(unique)} (from {len(RSS_SOURCES)} feeds)")
    return unique[:MAX_ARTICLES]
```

**Step 2: Verify the file is created**

```bash
python -c "import android; print('OK')"
```
Expected: `OK` (no import errors)

---

### Task 2: Add GitHub search functions to `android.py`

**Files:**
- Modify: `android.py` (append after `_fetch_rss_articles`)

**Context:** Copy the `_github_search` and `_parse_repo` functions from `github_trending.py` lines 53–119 verbatim — they are generic and reusable. Then add `_fetch_android_repos()` with Android-specific queries.

**Step 1: Append GitHub search + parse functions**

```python
def _github_search(query, sort="stars", per_page=30):
    """Search GitHub repos. Returns list of repo dicts."""
    params = {
        "q": query,
        "sort": sort,
        "order": "desc",
        "per_page": str(per_page),
    }
    url = f"{GH_SEARCH_URL}?{urllib.parse.urlencode(params)}"
    print(f"  GitHub Search: {query}")
    headers = {
        "User-Agent": "eof.news Android Tracker",
        "Accept": "application/vnd.github+json",
    }
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            remaining = resp.headers.get("X-RateLimit-Remaining", "?")
            print(f"    Rate limit remaining: {remaining}")
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 401 and token:
            print(f"    Token rejected, retrying without auth...")
            headers.pop("Authorization", None)
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
            except Exception as e2:
                print(f"    GitHub Search error: {e2}")
                return []
        else:
            print(f"    GitHub Search error: {e}")
            return []
    except Exception as e:
        print(f"    GitHub Search error: {e}")
        return []
    return data.get("items", [])


def _parse_repo(item):
    """Parse a GitHub Search API repo item into our schema."""
    owner = item.get("owner", {})
    license_info = item.get("license") or {}
    return {
        "name": item.get("full_name", ""),
        "description": (item.get("description") or "")[:200],
        "stars": item.get("stargazers_count", 0),
        "forks": item.get("forks_count", 0),
        "open_issues": item.get("open_issues_count", 0),
        "language": item.get("language") or "Unknown",
        "license": license_info.get("spdx_id") or "Unknown",
        "last_push": item.get("pushed_at", ""),
        "created_at": item.get("created_at", ""),
        "owner_url": owner.get("html_url", ""),
        "owner_avatar": owner.get("avatar_url", ""),
        "owner_login": owner.get("login", ""),
        "repo_url": item.get("html_url", ""),
        "topics": item.get("topics", [])[:8],
    }


def _fetch_android_repos():
    """Fetch Android/Kotlin repos from GitHub Search API. Returns deduplicated list."""
    now = datetime.now(timezone.utc)
    three_months_ago = (now - timedelta(days=90)).strftime("%Y-%m-%d")
    month_ago = (now - timedelta(days=30)).strftime("%Y-%m-%d")

    print("Fetching Android GitHub repositories...")

    # Established Android/Kotlin repos sorted by stars
    top_android = _github_search(
        "topic:android language:kotlin stars:>100", sort="stars", per_page=20
    )
    # Actively updated Jetpack Compose repos
    compose_repos = _github_search(
        f"topic:jetpack-compose pushed:>{three_months_ago} stars:>30",
        sort="stars", per_page=15
    )
    # New Android repos gaining traction
    new_android = _github_search(
        f"topic:android created:>{month_ago} stars:>10", sort="stars", per_page=15
    )

    seen = set()
    repos = []
    new_names = {item.get("full_name", "") for item in new_android}
    for item in top_android + compose_repos + new_android:
        name = item.get("full_name", "")
        if name and name not in seen:
            seen.add(name)
            repo = _parse_repo(item)
            repo["is_discovery"] = name in new_names
            repos.append(repo)

    repos.sort(key=lambda r: r["stars"], reverse=True)
    repos = repos[:25]
    print(f"  Total unique Android repos: {len(repos)}")
    return repos
```

**Step 2: Smoke test the search functions**

```bash
python -c "
from android import _fetch_android_repos
repos = _fetch_android_repos()
print(f'Got {len(repos)} repos')
print(repos[0]['name'], repos[0]['stars'])
"
```
Expected: prints a count (≥ 1) and a repo name + stars number. Network errors are fine if GitHub returns results.

---

### Task 3: Add history + delta + Repo of the Day functions to `android.py`

**Files:**
- Modify: `android.py` (append)

**Context:** These are identical in logic to `github_trending.py` lines 122–208. Copy with the history file path pointing to `HISTORY_JSON` (which is `docs/_data/android_history.json`).

**Step 1: Append history functions**

```python
def _load_history():
    if os.path.exists(HISTORY_JSON):
        try:
            with open(HISTORY_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"snapshots": {}, "featured_repos": {}}


def _save_history(history):
    cutoff = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%d")
    history["snapshots"] = {k: v for k, v in history["snapshots"].items() if k >= cutoff}
    history["featured_repos"] = {k: v for k, v in history["featured_repos"].items() if v >= cutoff}
    with open(HISTORY_JSON, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    print(f"  History written: {HISTORY_JSON}")


def _record_snapshot(repos, history):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    snapshot = {r["name"]: {"stars": r["stars"], "forks": r["forks"]} for r in repos}
    history["snapshots"][today] = {"repos": snapshot}


def _compute_deltas(repos, history):
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_snapshot = history["snapshots"].get(yesterday, {}).get("repos", {})
    deltas = {}
    for repo in repos:
        name = repo["name"]
        if name not in yesterday_snapshot:
            deltas[name] = {"star_delta": 0, "badge": "new_entry"}
        else:
            delta = repo["stars"] - yesterday_snapshot[name].get("stars", 0)
            if delta >= STAR_DELTA_RISING_THRESHOLD:
                badge = "rising"
            elif delta <= 0:
                badge = "cooling"
            else:
                badge = None
            deltas[name] = {"star_delta": delta, "badge": badge}
    return deltas


def _pick_repo_of_the_day(repos, deltas, history):
    featured = history.get("featured_repos", {})
    cutoff = (datetime.now(timezone.utc) - timedelta(days=FEATURED_COOLDOWN_DAYS)).strftime("%Y-%m-%d")
    recent_featured = {k for k, v in featured.items() if v >= cutoff}

    recent_by_date = sorted(
        [(k, v) for k, v in featured.items() if v >= cutoff],
        key=lambda x: x[1], reverse=True
    )[:3]
    recent_languages = set()
    for fname, _ in recent_by_date:
        for r in repos:
            if r["name"] == fname:
                recent_languages.add(r["language"])
                break

    candidates = [r for r in repos if r["name"] not in recent_featured] or repos

    def sort_key(r):
        delta = deltas.get(r["name"], {}).get("star_delta", 0)
        lang_bonus = 1 if r["language"] not in recent_languages else 0
        discovery_bonus = 2 if r.get("is_discovery") else 0
        return (discovery_bonus, delta, lang_bonus, r["stars"])

    candidates.sort(key=sort_key, reverse=True)
    return candidates[0] if candidates else None
```

**Step 2: Verify the module still imports cleanly**

```bash
python -c "import android; print('history/delta functions OK')"
```
Expected: `history/delta functions OK`

---

### Task 4: Add `_generate_page()` to `android.py`

**Files:**
- Modify: `android.py` (append)

**Context:** This generates the Jekyll markdown. The page uses `site.data.android.*` Liquid variables (NOT `site.data.github.*`). Keep charts simple: language donut + top repos bar. Articles rendered with plain cards. Repos rendered with the same card style as `/github/`.

**Step 1: Append `_generate_page` function**

```python
def _generate_page(repos, featured, deltas, articles):
    """Generate the Jekyll markdown page for /android/."""
    lang_counts = Counter(r["language"] for r in repos if r["language"] != "Unknown")
    top_langs = lang_counts.most_common(8)
    lang_labels = json.dumps([l[0] for l in top_langs])
    lang_data = json.dumps([l[1] for l in top_langs])
    lang_colors = json.dumps([LANGUAGE_COLORS.get(l[0], "#9ca3af") for l in top_langs])

    top10 = repos[:10]
    bar_labels = json.dumps([r["name"].split("/")[-1][:20] for r in top10])
    bar_data = json.dumps([r["stars"] for r in top10])

    top_language = top_langs[0][0] if top_langs else "Kotlin"
    most_starred = repos[0] if repos else None

    lines = [
        "---",
        "layout: page",
        'title: "Android Dev Hub"',
        'description: "Trending Android repositories and curated news for Android developers. Kotlin, Jetpack Compose, and the Android ecosystem — updated daily."',
        "permalink: /android/",
        "---",
        "",
        "## Overview",
        "",
        "{% assign repos = site.data.android.repos %}",
        "{% assign articles = site.data.android.articles %}",
        "{% assign featured = site.data.android.featured_repo %}",
        "",
        '<div style="display:flex; gap:1em; flex-wrap:wrap; margin-bottom:1.5em;">',
        '  <a href="#trending-repos" style="padding:4px 12px; border-radius:12px; background:#dbeafe; color:#1e40af; font-weight:bold; text-decoration:none; cursor:pointer;">Repos: {{ repos.size }}</a>',
        '  <a href="#android-news" style="padding:4px 12px; border-radius:12px; background:#dcfce7; color:#166534; font-weight:bold; text-decoration:none; cursor:pointer;">Articles: {{ articles.size }}</a>',
    ]

    if most_starred:
        lines.append(
            f'  <a href="{most_starred["repo_url"]}" target="_blank" rel="noopener" style="padding:4px 12px; border-radius:12px; background:#fef3c7; color:#92400e; font-weight:bold; text-decoration:none; cursor:pointer;">'
            f'Top Language: {top_language}</a>'
        )

    lines += ["</div>", ""]

    # Repo of the Day
    if featured:
        fd = deltas.get(featured["name"], {})
        delta_val = fd.get("star_delta", 0)
        delta_str = f"+{delta_val}" if delta_val > 0 else str(delta_val)
        topic_html = ""
        if featured.get("topics"):
            topic_html = '<div style="margin-top:0.5em;">' + " ".join(
                f'<a href="/tags/{t}/" style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#fef3c7; border-radius:6px; color:#92400e; font-size:0.75em; text-decoration:none;">{t}</a>'
                for t in featured["topics"]
            ) + "</div>"

        lines += [
            "## \U0001f4f1 Repo of the Day",
            "",
            '<div style="margin-bottom:1.5em; padding:1em; border:2px solid #a855f7; border-radius:12px; background:#faf5ff;">',
            '  <div style="display:flex; align-items:center; gap:0.5em; margin-bottom:0.5em; flex-wrap:wrap;">',
            f'    <img src="{featured["owner_avatar"]}&s=32" alt="" width="32" height="32" style="border-radius:50%;">',
            f'    <strong style="font-size:1.2em;"><a href="{featured["repo_url"]}" target="_blank" rel="noopener">{featured["name"]}</a></strong>',
            f'    <a href="{featured["repo_url"]}" target="_blank" rel="noopener" style="padding:2px 8px; border-radius:12px; font-size:0.8em; background:#a855f7; color:#fff; text-decoration:none;">\u2b50 Repo of the Day</a>',
            f'    <span style="font-size:0.85em; color:#7e22ce;">{delta_str} stars today</span>',
            "  </div>",
            f'  <p style="margin:0.3em 0; color:#374151;">{featured["description"]}</p>',
            '  <div style="display:flex; gap:1em; font-size:0.85em; color:#6b7280; flex-wrap:wrap;">',
            f'    <span>&#9733; {featured["stars"]:,}</span>',
            f'    <span>&#127860; {featured["forks"]:,}</span>',
            f'    <span>{featured["language"]}</span>',
            f'    <span>{featured["license"]}</span>',
            "  </div>",
            f"  {topic_html}",
            "</div>",
            "",
        ]

    # Charts
    lines += [
        "## Charts",
        "",
        '<div style="display:flex; gap:2em; flex-wrap:wrap; margin-bottom:2em;">',
        '  <div style="flex:1; min-width:280px; max-width:400px;">',
        '    <h3 style="font-size:1rem; margin-bottom:0.5rem;">Language Distribution</h3>',
        '    <canvas id="langChart" width="380" height="380"></canvas>',
        "  </div>",
        '  <div style="flex:2; min-width:300px;">',
        '    <h3 style="font-size:1rem; margin-bottom:0.5rem;">Top Repos by Stars</h3>',
        '    <canvas id="starsChart" width="600" height="380"></canvas>',
        "  </div>",
        "</div>",
        "",
        '<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>',
        "<script>",
        "new Chart(document.getElementById('langChart'), {",
        "  type: 'doughnut',",
        "  data: {",
        f"    labels: {lang_labels},",
        f"    datasets: [{{ data: {lang_data}, backgroundColor: {lang_colors} }}]",
        "  },",
        "  options: { responsive: true, plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, padding: 8, font: { size: 11 } } } } }",
        "});",
        "new Chart(document.getElementById('starsChart'), {",
        "  type: 'bar',",
        "  data: {",
        f"    labels: {bar_labels},",
        f"    datasets: [{{ label: 'Stars', data: {bar_data}, backgroundColor: '#a855f7', borderRadius: 4 }}]",
        "  },",
        "  options: {",
        "    indexAxis: 'y', responsive: true,",
        "    plugins: { legend: { display: false } },",
        "    scales: { x: { ticks: { callback: function(v) { return v >= 1000 ? (v/1000).toFixed(0) + 'k' : v; } } } }",
        "  }",
        "});",
        "</script>",
        "",
    ]

    # Android News section
    lines += [
        "## Latest Android News {#android-news}",
        "",
        "{% for article in articles %}",
        '<div style="margin-bottom:1em; padding:0.75em; border:1px solid #e5e7eb; border-radius:8px;">',
        '  <div style="display:flex; align-items:baseline; gap:0.5em; flex-wrap:wrap; margin-bottom:0.25em;">',
        '    <strong><a href="{{ article.url }}" target="_blank" rel="noopener">{{ article.title }}</a></strong>',
        '  </div>',
        '  <p style="margin:0.25em 0; font-size:0.88em; color:#374151;">{{ article.excerpt }}</p>',
        '  <span style="font-size:0.78em; color:#9ca3af;">{{ article.source }} &middot; {{ article.published | slice: 0, 10 }}</span>',
        "</div>",
        "{% endfor %}",
        "",
    ]

    # Trending repos section
    lines += [
        "## Trending Android Repos {#trending-repos}",
        "",
        "{% for repo in repos %}",
        '<div style="margin-bottom:1.2em; padding:0.75em; border:1px solid #e5e7eb; border-radius:8px;">',
        '  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap;">',
        '    <img src="{{ repo.owner_avatar }}&s=24" alt="" width="24" height="24" style="border-radius:50%;" loading="lazy">',
        '    <strong><a href="{{ repo.repo_url }}" target="_blank" rel="noopener">{{ repo.name }}</a></strong>',
        "    {% if repo.language %}",
        '      <span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; background:{% if repo.language == \'Kotlin\' %}#A97BFF{% elsif repo.language == \'Java\' %}#b07219{% elsif repo.language == \'C++\' %}#f34b7d{% elsif repo.language == \'Dart\' %}#00B4AB{% else %}#6b7280{% endif %};">{{ repo.language }}</span>',
        "    {% endif %}",
        '    {% if repo.badge == "new_entry" %}',
        '      <a href="{{ repo.repo_url }}" target="_blank" rel="noopener" style="padding:2px 8px; border-radius:12px; font-size:0.75em; text-decoration:none; background:#dbeafe; color:#1e40af; font-weight:bold;">\U0001f195 NEW</a>',
        '    {% elsif repo.badge == "rising" %}',
        '      <a href="{{ repo.repo_url }}" target="_blank" rel="noopener" style="padding:2px 8px; border-radius:12px; font-size:0.75em; text-decoration:none; background:#dcfce7; color:#166534; font-weight:bold;">\U0001f4c8 +{{ repo.star_delta }}</a>',
        '    {% elsif repo.badge == "cooling" %}',
        '      <a href="{{ repo.repo_url }}" target="_blank" rel="noopener" style="padding:2px 8px; border-radius:12px; font-size:0.75em; text-decoration:none; background:#fee2e2; color:#991b1b; font-weight:bold;">\U0001f4c9 {{ repo.star_delta }}</a>',
        "    {% endif %}",
        "  </div>",
        '  <p style="margin:0.3em 0; font-size:0.9em; color:#374151;">{{ repo.description }}</p>',
        '  <span style="font-size:0.85em; color:#6b7280;">',
        "    &#9733; {{ repo.stars }}",
        "    &middot; &#127860; {{ repo.forks }}",
        "    &middot; Updated: {{ repo.last_push | date: '%b %d, %Y' }}",
        '    {% if repo.star_delta != 0 %}&middot; <span style="color:{% if repo.star_delta > 0 %}#16a34a{% else %}#dc2626{% endif %};">{% if repo.star_delta > 0 %}+{% endif %}{{ repo.star_delta }} today</span>{% endif %}',
        "  </span>",
        "  {% if repo.topics.size > 0 %}",
        '  <br><span style="font-size:0.75em;">',
        "    {% for topic in repo.topics %}",
        '      {% assign topic_slug = topic | slugify %}<a href="/tags/{{ topic_slug }}/" style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#f3f4f6; border-radius:6px; color:#374151; text-decoration:none;">{{ topic }}</a>',
        "    {% endfor %}",
        "  </span>",
        "  {% endif %}",
        "</div>",
        "{% endfor %}",
        "",
        "---",
        "",
        '<p style="font-size:0.8em; color:#9ca3af;">',
        'Data from <a href="https://github.com">GitHub</a> Search API &amp; RSS feeds &middot; Updated: {{ site.data.android.generated_at }}',
        "</p>",
        "",
    ]

    return "\n".join(lines)
```

**Step 2: Verify the function exists**

```bash
python -c "from android import _generate_page; print('_generate_page OK')"
```
Expected: `_generate_page OK`

---

### Task 5: Add `publish_android()` entry point to `android.py`

**Files:**
- Modify: `android.py` (append)

**Step 1: Append `publish_android` function**

```python
def publish_android():
    """Main entry point: fetch data, compute stats, generate outputs."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=== Android Tracker ===")
    articles = _fetch_rss_articles()
    repos = _fetch_android_repos()

    history = _load_history()
    deltas = _compute_deltas(repos, history)
    featured = _pick_repo_of_the_day(repos, deltas, history)

    for repo in repos:
        d = deltas.get(repo["name"], {})
        repo["star_delta"] = d.get("star_delta", 0)
        repo["badge"] = d.get("badge")

    _record_snapshot(repos, history)
    if featured:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        history["featured_repos"][featured["name"]] = today
        print(f"  Repo of the Day: {featured['name']}")
    _save_history(history)

    lang_counts = Counter(r["language"] for r in repos if r["language"] != "Unknown")
    top_language = lang_counts.most_common(1)[0][0] if lang_counts else "Kotlin"

    now = datetime.now(timezone.utc)
    output = {
        "generated_at": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "total_repos": len(repos),
        "total_articles": len(articles),
        "top_language": top_language,
        "featured_repo": featured,
        "repos": repos,
        "articles": articles,
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"  JSON written: {OUTPUT_JSON}")

    page_content = _generate_page(repos, featured, deltas, articles)
    with open(OUTPUT_PAGE, "w", encoding="utf-8") as f:
        f.write(page_content)
    print(f"  Page written: {OUTPUT_PAGE}")
    print("=== Done ===")
```

**Step 2: Run a full end-to-end test**

```bash
python main.py --action=android
```

Expected output (approximate):
```
=== Android Tracker ===
  Articles fetched: N (from 5 feeds)
  GitHub Search: topic:android language:kotlin stars:>100
    Rate limit remaining: ...
  ...
  Total unique Android repos: N
  Repo of the Day: some/repo
  History written: docs/_data/android_history.json
  JSON written: docs/_data/android.json
  Page written: docs/android/index.md
=== Done ===
```

**Step 3: Verify outputs exist and are valid**

```bash
python -c "
import json
data = json.load(open('docs/_data/android.json'))
print('repos:', len(data['repos']))
print('articles:', len(data['articles']))
print('featured:', data.get('featured_repo', {}).get('name'))
print('generated_at:', data['generated_at'])
"
```

Expected: all fields populated, repos ≥ 1, articles ≥ 0.

**Step 4: Spot-check the generated page**

Open `docs/android/index.md` in a text editor and verify:
- Front matter has `permalink: /android/`
- Repo of the Day section present (with the featured repo name)
- `{% for article in articles %}` and `{% for repo in repos %}` blocks present

---

### Task 6: Wire `android` into `main.py`

**Files:**
- Modify: `main.py`

**Context:** `main.py` currently has cases for `news`, `digest`, `cves`, `models`, `github`, `outages`, `bootleg`. Add `android`.

**Step 1: Add case in `main.py`**

In `main.py`, add after the `case "outages":` block (around line 22):

```python
        case "android":
            from android import publish_android
            publish_android()
```

Also update the argparse help string on line 34:
```python
    parser.add_argument("--action", type=str, default="news", help="Action: news, digest, cves, models, github, bootleg, outages, android")
```

**Step 2: Verify**

```bash
python main.py --action=android
```
Expected: same output as Task 5 Step 2. No `ModuleNotFoundError`.

---

### Task 7: Add nav link to header

**Files:**
- Modify: `docs/_includes/header.html`

**Context:** Current nav items (line 19–26): Home, GitHub, Models, Bootleg, Outages, CVEs, Digest. Add Android after GitHub.

**Step 1: Add the nav link**

In `docs/_includes/header.html`, after:
```html
        <a class="nav-item" href="/github/">GitHub</a>
```

Add:
```html
        <a class="nav-item" href="/android/">Android</a>
```

**Step 2: Visually verify**

Open `docs/_includes/header.html` and confirm the new link is between GitHub and Models.

---

### Task 8: Create the GitHub Actions workflow

**Files:**
- Create: `.github/workflows/androidtracker.yml`

**Context:** Copy the structure of `.github/workflows/githubtrending.yml` exactly, changing the job name, step names, run command, and schedule.

**Step 1: Create the workflow file**

```yaml
name: Android Dev Tracker

on:
  schedule:
    - cron: '0 8 * * *'   # 08:00 UTC = 09:00 Rome - Daily
  workflow_dispatch:

jobs:
  run-android:
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

    - name: Run Android tracker
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: python main.py --action=android

    - name: Commit and Push changes
      run: |
        find . -type d -name "__pycache__" -exec rm -r {} +
        find . -name "*.pyc" -delete
        git add .
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
        git commit -m "Auto: Android tracker update at $TIMESTAMP" || echo "No changes to commit"
        git push origin main
```

**Step 2: Verify the workflow file is valid YAML**

```bash
python -c "
import yaml
with open('.github/workflows/androidtracker.yml') as f:
    data = yaml.safe_load(f)
print('schedule:', data['on']['schedule'])
print('job:', list(data['jobs'].keys()))
"
```
Expected: schedule printed + `['run-android']`

Note: if `yaml` is not installed, just visually check the indentation is correct.

---

### Task 9: Final verification

**Step 1: Check all new/modified files exist**

```bash
ls -la android.py docs/_data/android.json docs/_data/android_history.json docs/android/index.md .github/workflows/androidtracker.yml
```

**Step 2: Verify Jekyll front matter is correct**

```bash
python -c "
with open('docs/android/index.md') as f:
    content = f.read()
assert 'permalink: /android/' in content, 'permalink missing'
assert 'layout: page' in content, 'layout missing'
assert 'site.data.android.repos' in content, 'liquid variable missing'
assert 'site.data.android.articles' in content, 'articles variable missing'
print('Jekyll front matter OK')
"
```

**Step 3: Verify JSON schema**

```bash
python -c "
import json
data = json.load(open('docs/_data/android.json'))
assert 'repos' in data
assert 'articles' in data
assert 'featured_repo' in data
assert 'generated_at' in data
repo = data['repos'][0]
assert all(k in repo for k in ['name','stars','forks','language','repo_url','badge','star_delta'])
print('JSON schema OK')
print(f'  {len(data[\"repos\"])} repos, {len(data[\"articles\"])} articles')
"
```

**Step 4: Check header link was added**

```bash
python -c "
content = open('docs/_includes/header.html').read()
assert '/android/' in content, 'nav link missing'
print('Nav link OK')
"
```

**Step 5: Check `main.py` has the android case**

```bash
python -c "
content = open('main.py').read()
assert 'case \"android\"' in content
print('main.py case OK')
"
```

All checks pass? The Android section is complete.
