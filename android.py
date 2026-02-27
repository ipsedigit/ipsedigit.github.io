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

LANGUAGE_COLORS = {
    "Kotlin": "#A97BFF",
    "Java":   "#b07219",
    "C++":    "#f34b7d",
    "C":      "#555555",
    "Python": "#3572A5",
    "Dart":   "#00B4AB",
    "Swift":  "#F05138",
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

    seen_urls = set()
    unique = []
    articles.sort(key=lambda a: a["published"], reverse=True)
    for a in articles:
        if a["url"] not in seen_urls:
            seen_urls.add(a["url"])
            unique.append(a)

    print(f"  Articles fetched: {len(unique)} (from {len(RSS_SOURCES)} feeds)")
    return unique[:MAX_ARTICLES]


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

    top_android = _github_search(
        "topic:android language:kotlin stars:>100", sort="stars", per_page=20
    )
    compose_repos = _github_search(
        f"topic:jetpack-compose pushed:>{three_months_ago} stars:>30",
        sort="stars", per_page=15
    )
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
        "{% assign repos = site.data.android.repos %}",
        "{% assign articles = site.data.android.articles %}",
        "",
        '<div style="display:flex; gap:1em; flex-wrap:wrap; margin-bottom:1.5em;">',
        '  <a href="#trending-repos" style="padding:4px 12px; border-radius:12px; background:#dbeafe; color:#1e40af; font-weight:bold; text-decoration:none; cursor:pointer;">Repos: {{ repos.size }}</a>',
        '  <a href="#android-news" style="padding:4px 12px; border-radius:12px; background:#dcfce7; color:#166534; font-weight:bold; text-decoration:none; cursor:pointer;">Articles: {{ articles.size }}</a>',
    ]

    if most_starred:
        lines.append(
            f'  <span style="padding:4px 12px; border-radius:12px; background:#fef3c7; color:#92400e; font-weight:bold;">Top Language: {top_language}</span>'
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
                f'<a href="/tags/{t}/" style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#f3e8ff; border-radius:6px; color:#7e22ce; font-size:0.75em; text-decoration:none;">{t}</a>'
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
        "## Latest Android News {#android-news}",
        "",
        "{% for article in articles %}",
        '<div style="margin-bottom:1em; padding:0.75em; border:1px solid #e5e7eb; border-radius:8px;">',
        '  <strong><a href="{{ article.url }}" target="_blank" rel="noopener">{{ article.title }}</a></strong>',
        '  <p style="margin:0.25em 0; font-size:0.88em; color:#374151;">{{ article.excerpt }}</p>',
        '  <span style="font-size:0.78em; color:#9ca3af;">{{ article.source }} &middot; {{ article.published | slice: 0, 10 }}</span>',
        "</div>",
        "{% endfor %}",
        "",
        "## Trending Android Repos {#trending-repos}",
        "",
        "{% for repo in repos %}",
        '<div style="margin-bottom:1.2em; padding:0.75em; border:1px solid #e5e7eb; border-radius:8px;">',
        '  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap;">',
        '    <img src="{{ repo.owner_avatar }}&s=24" alt="" width="24" height="24" style="border-radius:50%;" loading="lazy">',
        '    <strong><a href="{{ repo.repo_url }}" target="_blank" rel="noopener">{{ repo.name }}</a></strong>',
        "    {% if repo.language %}",
        "      {% assign lang_slug = repo.language | slugify %}",
        '      <a href="/tags/{{ lang_slug }}/" style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; text-decoration:none; background:{% if repo.language == \'Kotlin\' %}#A97BFF{% elsif repo.language == \'Java\' %}#b07219{% elsif repo.language == \'C++\' %}#f34b7d{% elsif repo.language == \'Dart\' %}#00B4AB{% elsif repo.language == \'Swift\' %}#F05138{% else %}#6b7280{% endif %};">{{ repo.language }}</a>',
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
