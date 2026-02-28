"""
GitHub Trending Tracker.
Fetches trending repositories from GitHub Search API
and generates docs/_data/github.json and docs/github/trending.md.
"""
import json
import os
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timezone, timedelta
from collections import Counter

DATA_DIR = "docs/_data"
OUTPUT_JSON = os.path.join(DATA_DIR, "github.json")
OUTPUT_DIR = "docs/github"
OUTPUT_PAGE = os.path.join(OUTPUT_DIR, "trending.md")
HISTORY_JSON = os.path.join(DATA_DIR, "github_history.json")
STAR_DELTA_RISING_THRESHOLD = 50   # stars gained in 24h to qualify as "rising"
FEATURED_COOLDOWN_DAYS = 30

GH_SEARCH_URL = "https://api.github.com/search/repositories"

LANGUAGE_COLORS = {
    "Python": "#3572A5",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "Rust": "#dea584",
    "Go": "#00ADD8",
    "Java": "#b07219",
    "C++": "#f34b7d",
    "C": "#555555",
    "C#": "#178600",
    "Ruby": "#701516",
    "Swift": "#F05138",
    "Kotlin": "#A97BFF",
    "PHP": "#4F5D95",
    "Scala": "#c22d40",
    "Shell": "#89e051",
    "Jupyter Notebook": "#DA5B0B",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Dart": "#00B4AB",
    "Lua": "#000080",
    "Zig": "#ec915c",
    "Elixir": "#6e4a7e",
    "Haskell": "#5e5086",
    "Vue": "#41b883",
    "Svelte": "#ff3e00",
}


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
        "User-Agent": "eof.news GitHub Tracker",
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
            data = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code == 401 and token:
            # Token invalid/expired — retry without auth
            print(f"    Token rejected, retrying without auth...")
            headers.pop("Authorization", None)
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
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


def _load_history():
    """Load history file. Returns dict with 'snapshots' and 'featured_repos' keys."""
    if os.path.exists(HISTORY_JSON):
        try:
            with open(HISTORY_JSON, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"snapshots": {}, "featured_repos": {}}


def _save_history(history):
    """Save history, pruning snapshots older than 30 days."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%d")
    history["snapshots"] = {k: v for k, v in history["snapshots"].items() if k >= cutoff}
    history["featured_repos"] = {k: v for k, v in history["featured_repos"].items() if v >= cutoff}

    with open(HISTORY_JSON, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    print(f"  History written: {HISTORY_JSON} ({len(history['snapshots'])} snapshots)")


def _record_snapshot(repos, history):
    """Record today's snapshot into history."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    snapshot = {}
    for r in repos:
        snapshot[r["name"]] = {"stars": r["stars"], "forks": r["forks"]}
    history["snapshots"][today] = {"repos": snapshot}


def _compute_deltas(repos, history):
    """Compare today's repos against yesterday's snapshot. Returns dict of deltas and badges."""
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_snapshot = history["snapshots"].get(yesterday, {}).get("repos", {})

    deltas = {}
    for repo in repos:
        name = repo["name"]
        today_stars = repo["stars"]
        if name not in yesterday_snapshot:
            deltas[name] = {"star_delta": 0, "badge": "new_entry"}
        else:
            prev_stars = yesterday_snapshot[name].get("stars", 0)
            delta = today_stars - prev_stars
            if delta >= STAR_DELTA_RISING_THRESHOLD:
                badge = "rising"
            elif delta <= 0:
                badge = "cooling"
            else:
                badge = None
            deltas[name] = {"star_delta": delta, "badge": badge}

    return deltas


def _pick_repo_of_the_day(repos, deltas, history):
    """Select featured repo: not featured recently, highest momentum, language diversity."""
    featured = history.get("featured_repos", {})
    cutoff = (datetime.now(timezone.utc) - timedelta(days=FEATURED_COOLDOWN_DAYS)).strftime("%Y-%m-%d")

    recent_featured = {k for k, v in featured.items() if v >= cutoff}

    # Get languages of last 3 featured repos
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

    candidates = [r for r in repos if r["name"] not in recent_featured]
    if not candidates:
        candidates = repos

    def sort_key(r):
        delta = deltas.get(r["name"], {}).get("star_delta", 0)
        lang_bonus = 1 if r["language"] not in recent_languages else 0
        discovery_bonus = 2 if r.get("is_discovery") else 0
        return (discovery_bonus, delta, lang_bonus, r["stars"])

    candidates.sort(key=sort_key, reverse=True)
    return candidates[0] if candidates else None


def _fetch_trending_repos():
    """Fetch trending repos from multiple GitHub Search queries. Returns deduplicated list."""
    now = datetime.now(timezone.utc)
    week_ago = (now - timedelta(days=7)).strftime("%Y-%m-%d")
    three_days_ago = (now - timedelta(days=3)).strftime("%Y-%m-%d")
    six_months_ago = (now - timedelta(days=180)).strftime("%Y-%m-%d")

    print("Fetching trending GitHub repositories...")

    # Query 1: New repos this week, sorted by stars
    new_this_week = _github_search(f"created:>{week_ago} stars:>10", sort="stars", per_page=20)

    # Query 2: Most starred repos updated in last 3 days
    recently_active = _github_search(f"pushed:>{three_days_ago} stars:>1000", sort="stars", per_page=20)

    # Query 3: Newcomers — created in last 6 months, growing fast
    newcomers = _github_search(f"created:>{six_months_ago} stars:>100", sort="stars", per_page=20)

    # Query 4: Discovery — small explosive repos (created last 2 weeks, stars > 20)
    two_weeks_ago = (now - timedelta(days=14)).strftime("%Y-%m-%d")
    discovery = _github_search(f"created:>{two_weeks_ago} stars:>20", sort="stars", per_page=15)

    # Deduplicate by full_name
    seen = set()
    repos = []
    discovery_names = {item.get("full_name", "") for item in discovery}
    for item in new_this_week + recently_active + newcomers + discovery:
        name = item.get("full_name", "")
        if name and name not in seen:
            seen.add(name)
            repo = _parse_repo(item)
            repo["is_discovery"] = name in discovery_names
            repos.append(repo)

    # Sort by stars descending
    repos.sort(key=lambda r: r["stars"], reverse=True)
    repos = repos[:30]

    print(f"  Total unique repos: {len(repos)}")
    return repos


def _generate_page(repos, featured, deltas, history=None):
    """Generate the Jekyll markdown page with Chart.js graphs."""
    if history is None:
        history = {"snapshots": {}, "featured_repos": {}}

    # Pre-compute stats for Chart.js (inline JSON in template)
    lang_counts = Counter(r["language"] for r in repos if r["language"] != "Unknown")
    top_langs = lang_counts.most_common(10)
    lang_labels = json.dumps([l[0] for l in top_langs])
    lang_data = json.dumps([l[1] for l in top_langs])
    lang_colors = json.dumps([LANGUAGE_COLORS.get(l[0], "#9ca3af") for l in top_langs])

    top10 = repos[:10]
    bar_labels = json.dumps([r["name"].split("/")[-1][:20] for r in top10])
    bar_data = json.dumps([r["stars"] for r in top10])

    # Top movers data for chart
    movers = sorted(
        [r for r in repos if r.get("star_delta", 0) != 0],
        key=lambda r: abs(r.get("star_delta", 0)),
        reverse=True
    )[:10]
    mover_labels = json.dumps([r["name"].split("/")[-1][:20] for r in movers])
    mover_data = json.dumps([r.get("star_delta", 0) for r in movers])
    mover_colors = json.dumps(["#16a34a" if r.get("star_delta", 0) > 0 else "#dc2626" for r in movers])

    # --- New entries per day (from history) ---
    snapshots = history.get("snapshots", {})
    sorted_dates = sorted(snapshots.keys())[-14:]  # last 14 days
    new_entries_labels = []
    new_entries_data = []
    for i, d in enumerate(sorted_dates):
        new_entries_labels.append(d[5:])  # "MM-DD"
        if i == 0:
            new_entries_data.append(0)
        else:
            prev_date = sorted_dates[i - 1]
            prev_names = set(snapshots[prev_date].get("repos", {}).keys())
            curr_names = set(snapshots[d].get("repos", {}).keys())
            new_entries_data.append(len(curr_names - prev_names))
    new_entries_labels_json = json.dumps(new_entries_labels)
    new_entries_data_json = json.dumps(new_entries_data)

    # --- Language trends over time (from history) ---
    # Track top 5 languages across all snapshots
    all_lang_counts = Counter()
    for d in sorted_dates:
        for rname, rdata in snapshots[d].get("repos", {}).items():
            pass  # snapshots only have stars/forks, not language
    # We need language from current repos - build a name->language map
    lang_map = {r["name"]: r["language"] for r in repos}
    top5_langs = [l[0] for l in lang_counts.most_common(5)]
    lang_trend_datasets = []
    lang_trend_colors = ["#3572A5", "#f1e05a", "#3178c6", "#dea584", "#00ADD8"]
    for idx, lang in enumerate(top5_langs):
        counts = []
        for d in sorted_dates:
            repo_names = set(snapshots[d].get("repos", {}).keys())
            count = sum(1 for n in repo_names if lang_map.get(n) == lang)
            counts.append(count)
        lang_trend_datasets.append({
            "label": lang,
            "data": counts,
            "borderColor": lang_trend_colors[idx % len(lang_trend_colors)],
            "backgroundColor": lang_trend_colors[idx % len(lang_trend_colors)] + "33",
            "fill": True,
            "tension": 0.3,
        })
    lang_trend_labels_json = json.dumps(new_entries_labels)  # same date labels
    lang_trend_datasets_json = json.dumps(lang_trend_datasets)

    # --- Activity heatmap (push day of week from current repos) ---
    day_counts = [0] * 7  # Mon=0 ... Sun=6
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for r in repos:
        if r.get("last_push"):
            try:
                push_dt = datetime.fromisoformat(r["last_push"].replace("Z", "+00:00"))
                day_counts[push_dt.weekday()] += 1
            except (ValueError, AttributeError):
                pass
    heatmap_labels_json = json.dumps(day_names)
    heatmap_data_json = json.dumps(day_counts)
    # Color intensity based on count
    max_count = max(day_counts) if day_counts else 1
    heatmap_colors_json = json.dumps([
        f"rgba(59, 130, 246, {max(0.2, c / max_count)})" for c in day_counts
    ])

    # --- Topic cloud (most common topics) ---
    topic_counts = Counter()
    for r in repos:
        for t in r.get("topics", []):
            topic_counts[t] += 1
    top_topics = topic_counts.most_common(20)
    max_topic = top_topics[0][1] if top_topics else 1

    lines = [
        "---",
        "layout: page",
        'title: "GitHub Hot Repos"',
        'description: "Hot GitHub repositories tracked daily. Stars, forks, languages, and contributors — the hottest open source projects right now."',
        "permalink: /github/",
        'title_badge: "⭐ GitHub"',
        'title_badge_bg: "#fef3c7"',
        'title_badge_color: "#92400e"',
        "---",
        "",
        "{% assign repos = site.data.github.repos %}",
        "{% assign top_lang = site.data.github.top_language %}",
        "{% assign most_starred = repos | first %}",
        "",
    ]

    # Repo of the Day section
    if featured:
        fd = deltas.get(featured["name"], {})
        delta_val = fd.get("star_delta", 0)
        delta_str = f"+{delta_val}" if delta_val > 0 else str(delta_val)
        topic_html = ""
        if featured.get("topics"):
            topic_html = '<div style="margin-top:0.5em;">' + ' '.join(
                f'<a href="/tags/{t}/" style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#fef3c7; border-radius:6px; color:#92400e; font-size:0.75em; text-decoration:none;">{t}</a>'
                for t in featured["topics"]
            ) + '</div>'

        lines += [
            '<div style="margin-bottom:1.5em; padding:1em; border:2px solid #f59e0b; border-radius:12px; background:#fffbeb;">',
            '  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap; margin-bottom:0.6em;">',
            '    <span style="padding:3px 10px; border-radius:12px; font-size:0.78em; font-weight:bold; background:#f59e0b; color:#fff;">&#9733; Latest</span>',
            f'    <span style="font-size:0.78em; color:#6b7280;">{delta_str} stars today</span>',
            '  </div>',
            '  <div style="display:flex; align-items:center; gap:0.5em; margin-bottom:0.5em; flex-wrap:wrap;">',
            f'    <img src="{featured["owner_avatar"]}&s=32" alt="" width="32" height="32" style="border-radius:50%;">',
            f'    <strong style="font-size:1.2em;"><a href="{featured["repo_url"]}" target="_blank" rel="noopener">{featured["name"]}</a></strong>',
            '  </div>',
            f'  <p style="margin:0.3em 0; color:#374151;">{featured["description"]}</p>',
            '  <div style="display:flex; gap:1em; font-size:0.85em; color:#6b7280; flex-wrap:wrap;">',
            f'    <span>&#9733; {featured["stars"]:,}</span>',
            f'    <span>&#127860; {featured["forks"]:,}</span>',
            f'    <span>{featured["language"]}</span>',
            f'    <span>{featured["license"]}</span>',
            '  </div>',
            f'  {topic_html}',
            '</div>',
            "",
        ]

    lines += [
        "{% for repo in repos %}",
        '<div style="margin-bottom:1.2em; padding:0.75em; border:1px solid #e5e7eb; border-radius:8px;">',
        '  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap;">',
        '    <img src="{{ repo.owner_avatar }}&s=24" alt="" width="24" height="24" style="border-radius:50%;" loading="lazy">',
        '    <strong><a href="{{ repo.repo_url }}" target="_blank" rel="noopener">{{ repo.name }}</a></strong>',
        "    {% if repo.language %}",
        "      {% assign lang_slug = repo.language | slugify %}",
        '      <a href="/tags/{{ lang_slug }}/" style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; text-decoration:none; background:{% if repo.language == \'Python\' %}#3572A5{% elsif repo.language == \'JavaScript\' %}#b08800{% elsif repo.language == \'TypeScript\' %}#3178c6{% elsif repo.language == \'Rust\' %}#dea584{% elsif repo.language == \'Go\' %}#00ADD8{% elsif repo.language == \'Java\' %}#b07219{% elsif repo.language == \'C++\' %}#f34b7d{% elsif repo.language == \'C\' %}#555{% elsif repo.language == \'C#\' %}#178600{% elsif repo.language == \'Ruby\' %}#701516{% elsif repo.language == \'Swift\' %}#F05138{% elsif repo.language == \'Kotlin\' %}#A97BFF{% else %}#6b7280{% endif %};">{{ repo.language }}</a>',
        "    {% endif %}",
        "    {% if repo.license != 'Unknown' %}",
        '      <a href="{{ repo.repo_url }}" target="_blank" rel="noopener" style="font-size:0.75em; color:#6b7280; border:1px solid #e5e7eb; padding:1px 6px; border-radius:8px; text-decoration:none;">{{ repo.license }}</a>',
        "    {% endif %}",
        '    {% if repo.badge == "new_entry" %}',
        '      <a href="{{ repo.repo_url }}" target="_blank" rel="noopener" style="padding:2px 8px; border-radius:12px; font-size:0.75em; text-decoration:none; background:#dbeafe; color:#1e40af; font-weight:bold;">\U0001f195 NEW</a>',
        '    {% elsif repo.badge == "rising" %}',
        '      <a href="{{ repo.repo_url }}" target="_blank" rel="noopener" style="padding:2px 8px; border-radius:12px; font-size:0.75em; text-decoration:none; background:#dcfce7; color:#166534; font-weight:bold;">\U0001f4c8 +{{ repo.star_delta }}</a>',
        '    {% elsif repo.badge == "cooling" %}',
        '      <a href="{{ repo.repo_url }}" target="_blank" rel="noopener" style="padding:2px 8px; border-radius:12px; font-size:0.75em; text-decoration:none; background:#fee2e2; color:#991b1b; font-weight:bold;">\U0001f4c9 {{ repo.star_delta }}</a>',
        '    {% endif %}',
        "  </div>",
        '  <p style="margin:0.3em 0; font-size:0.9em; color:#374151;">{{ repo.description }}</p>',
        '  <span style="font-size:0.85em; color:#6b7280;">',
        "    &#9733; {{ repo.stars }}",
        "    &middot; &#127860; {{ repo.forks }}",
        "    &middot; Issues: {{ repo.open_issues }}",
        "    &middot; Updated: {{ repo.last_push | date: '%b %d, %Y' }}",
        '    {% if repo.star_delta != 0 %}',
        '      &middot; <span style="color:{% if repo.star_delta > 0 %}#16a34a{% else %}#dc2626{% endif %};">',
        '        {% if repo.star_delta > 0 %}+{% endif %}{{ repo.star_delta }} today',
        '      </span>',
        '    {% endif %}',
        "  </span>",
        '  <br><span style="font-size:0.8em; color:#9ca3af;">',
        '    Owner: <a href="{{ repo.owner_url }}" target="_blank" rel="noopener" style="color:#6b7280;">{{ repo.owner_login }}</a>',
        "    &middot; Created: {{ repo.created_at | date: '%b %d, %Y' }}",
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
        'Data from <a href="https://github.com">GitHub</a> Search API &middot; Updated: {{ site.data.github.generated_at }}',
        "</p>",
        "",
    ]
    return "\n".join(lines)


def publish_github_trending():
    """Main entry point: fetch repos, compute deltas, pick featured, generate outputs."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    repos = _fetch_trending_repos()
    print(f"Total trending repos: {len(repos)}")

    # History-based computation
    history = _load_history()
    deltas = _compute_deltas(repos, history)
    featured = _pick_repo_of_the_day(repos, deltas, history)

    # Inject delta data into each repo dict
    for repo in repos:
        d = deltas.get(repo["name"], {})
        repo["star_delta"] = d.get("star_delta", 0)
        repo["badge"] = d.get("badge")

    # Record today's snapshot and featured repo
    _record_snapshot(repos, history)
    if featured:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        history["featured_repos"][featured["name"]] = today
        print(f"  Repo of the Day: {featured['name']}")
    _save_history(history)

    # Stats
    lang_counts = Counter(r["language"] for r in repos if r["language"] != "Unknown")
    top_language = lang_counts.most_common(1)[0][0] if lang_counts else "N/A"

    now = datetime.now(timezone.utc)
    output = {
        "generated_at": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "total": len(repos),
        "top_language": top_language,
        "repo_of_the_day": featured["name"] if featured else None,
        "repos": repos,
    }

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"  JSON written: {OUTPUT_JSON}")

    page_content = _generate_page(repos, featured, deltas, history)
    with open(OUTPUT_PAGE, 'w', encoding='utf-8') as f:
        f.write(page_content)
    print(f"  Page written: {OUTPUT_PAGE}")
