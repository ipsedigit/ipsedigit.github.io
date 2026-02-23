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

    # Deduplicate by full_name
    seen = set()
    repos = []
    for item in new_this_week + recently_active + newcomers:
        name = item.get("full_name", "")
        if name and name not in seen:
            seen.add(name)
            repos.append(_parse_repo(item))

    # Sort by stars descending
    repos.sort(key=lambda r: r["stars"], reverse=True)
    repos = repos[:30]

    print(f"  Total unique repos: {len(repos)}")
    return repos


def _generate_page(repos):
    """Generate the Jekyll markdown page with Chart.js graphs."""
    # Pre-compute stats for Chart.js (inline JSON in template)
    lang_counts = Counter(r["language"] for r in repos if r["language"] != "Unknown")
    top_langs = lang_counts.most_common(10)
    lang_labels = json.dumps([l[0] for l in top_langs])
    lang_data = json.dumps([l[1] for l in top_langs])
    lang_colors = json.dumps([LANGUAGE_COLORS.get(l[0], "#9ca3af") for l in top_langs])

    top10 = repos[:10]
    bar_labels = json.dumps([r["name"].split("/")[-1][:20] for r in top10])
    bar_data = json.dumps([r["stars"] for r in top10])

    lines = [
        "---",
        "layout: page",
        'title: "GitHub Hot Repos"',
        'description: "Hot GitHub repositories tracked daily. Stars, forks, languages, and contributors — the hottest open source projects right now."',
        "permalink: /github/",
        "---",
        "",
        "## Overview",
        "",
        "{% assign repos = site.data.github.repos %}",
        "{% assign top_lang = site.data.github.top_language %}",
        "{% assign most_starred = repos | first %}",
        "",
        '<div style="display:flex; gap:1em; flex-wrap:wrap; margin-bottom:1.5em;">',
        '  <span style="padding:4px 12px; border-radius:12px; background:#dbeafe; color:#1e40af; font-weight:bold;">Repos: {{ repos.size }}</span>',
        '  <span style="padding:4px 12px; border-radius:12px; background:#dcfce7; color:#166534; font-weight:bold;">Top Language: {{ top_lang }}</span>',
        '  {% if most_starred %}<span style="padding:4px 12px; border-radius:12px; background:#fef3c7; color:#92400e; font-weight:bold;">Most Starred: {{ most_starred.name }} ({{ most_starred.stars }})</span>{% endif %}',
        "</div>",
        "",
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
        "  options: {",
        "    responsive: true,",
        "    plugins: {",
        "      legend: { position: 'bottom', labels: { boxWidth: 12, padding: 8, font: { size: 11 } } }",
        "    }",
        "  }",
        "});",
        "new Chart(document.getElementById('starsChart'), {",
        "  type: 'bar',",
        "  data: {",
        f"    labels: {bar_labels},",
        f"    datasets: [{{ label: 'Stars', data: {bar_data}, backgroundColor: '#f59e0b', borderRadius: 4 }}]",
        "  },",
        "  options: {",
        "    indexAxis: 'y',",
        "    responsive: true,",
        "    plugins: { legend: { display: false } },",
        "    scales: { x: { ticks: { callback: function(v) { return v >= 1000 ? (v/1000).toFixed(0) + 'k' : v; } } } }",
        "  }",
        "});",
        "</script>",
        "",
        "## Trending Repositories",
        "",
        "{% for repo in repos %}",
        '<div style="margin-bottom:1.2em; padding:0.75em; border:1px solid #e5e7eb; border-radius:8px;">',
        '  <div style="display:flex; align-items:center; gap:0.5em;">',
        '    <img src="{{ repo.owner_avatar }}&s=24" alt="" width="24" height="24" style="border-radius:50%;" loading="lazy">',
        '    <strong><a href="{{ repo.repo_url }}" target="_blank" rel="noopener">{{ repo.name }}</a></strong>',
        "    {% if repo.language %}",
        '      <span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; background:{% if repo.language == \'Python\' %}#3572A5{% elsif repo.language == \'JavaScript\' %}#b08800{% elsif repo.language == \'TypeScript\' %}#3178c6{% elsif repo.language == \'Rust\' %}#dea584{% elsif repo.language == \'Go\' %}#00ADD8{% elsif repo.language == \'Java\' %}#b07219{% elsif repo.language == \'C++\' %}#f34b7d{% elsif repo.language == \'C\' %}#555{% elsif repo.language == \'C#\' %}#178600{% elsif repo.language == \'Ruby\' %}#701516{% elsif repo.language == \'Swift\' %}#F05138{% elsif repo.language == \'Kotlin\' %}#A97BFF{% else %}#6b7280{% endif %};">{{ repo.language }}</span>',
        "    {% endif %}",
        "    {% if repo.license != 'Unknown' %}",
        '      <span style="font-size:0.75em; color:#6b7280; border:1px solid #e5e7eb; padding:1px 6px; border-radius:8px;">{{ repo.license }}</span>',
        "    {% endif %}",
        "  </div>",
        '  <p style="margin:0.3em 0; font-size:0.9em; color:#374151;">{{ repo.description }}</p>',
        '  <span style="font-size:0.85em; color:#6b7280;">',
        "    &#9733; {{ repo.stars }}",
        "    &middot; &#127860; {{ repo.forks }}",
        "    &middot; Issues: {{ repo.open_issues }}",
        "    &middot; Updated: {{ repo.last_push | date: '%b %d, %Y' }}",
        "  </span>",
        '  <br><span style="font-size:0.8em; color:#9ca3af;">',
        '    Owner: <a href="{{ repo.owner_url }}" target="_blank" rel="noopener" style="color:#6b7280;">{{ repo.owner_login }}</a>',
        "    &middot; Created: {{ repo.created_at | date: '%b %d, %Y' }}",
        "  </span>",
        "  {% if repo.topics.size > 0 %}",
        '  <br><span style="font-size:0.75em;">',
        "    {% for topic in repo.topics %}",
        '      <span style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#f3f4f6; border-radius:6px; color:#374151;">{{ topic }}</span>',
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
    """Main entry point: fetch repos, generate JSON and page."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    repos = _fetch_trending_repos()
    print(f"Total trending repos: {len(repos)}")

    # Compute stats
    lang_counts = Counter(r["language"] for r in repos if r["language"] != "Unknown")
    top_language = lang_counts.most_common(1)[0][0] if lang_counts else "N/A"

    now = datetime.now(timezone.utc)
    output = {
        "generated_at": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "total": len(repos),
        "top_language": top_language,
        "repos": repos,
    }

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"  JSON written: {OUTPUT_JSON}")

    page_content = _generate_page(repos)
    with open(OUTPUT_PAGE, 'w', encoding='utf-8') as f:
        f.write(page_content)
    print(f"  Page written: {OUTPUT_PAGE}")
