import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta

import feedparser
import requests


# ── Helpers ───────────────────────────────────────────────────────────────────

def _parse_incident(raw: dict, service: str) -> dict:
    """Normalize a raw Statuspage incident dict."""
    return {
        "id":          raw.get("id", ""),
        "name":        raw.get("name", ""),
        "status":      raw.get("status", ""),
        "impact":      raw.get("impact", ""),
        "service":     service,
        "started_at":  raw.get("started_at") or raw.get("created_at", ""),
        "updated_at":  raw.get("updated_at", ""),
        "resolved_at": raw.get("resolved_at"),
        "shortlink":   raw.get("shortlink", ""),
    }


def _is_recent_resolved(inc: dict) -> bool:
    """Return True if incident was resolved in the last 24 hours."""
    resolved_at = inc.get("resolved_at")
    if not resolved_at:
        return False
    try:
        resolved_dt = datetime.fromisoformat(resolved_at.replace("Z", "+00:00"))
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        return resolved_dt > cutoff
    except (ValueError, AttributeError):
        return False


def _generate_page(active: list, resolved: list, timestamp: str) -> str:
    """Generate the HTML fragment for the incidents section."""
    parts = []

    # Banner
    if not active:
        parts.append(
            '<div class="outage-banner outage-banner--ok">'
            '<span class="outage-banner__icon">✓</span>'
            ' All systems operational'
            '</div>'
        )
    else:
        count = len(active)
        label = f"{count} active incident{'s' if count != 1 else ''}"
        parts.append(
            f'<div class="outage-banner outage-banner--warn">'
            f'<span class="outage-banner__icon">⚠</span>'
            f' {label}'
            f'</div>'
        )

    # Active incidents
    if active:
        parts.append(
            '<div class="outage-section">'
            '<div class="section-head"><span class="section-label">Active Incidents</span>'
            '<div class="section-line"></div></div>'
            '<div class="outage-list">'
        )
        for inc in active:
            impact = inc.get("impact", "").upper()
            name   = inc.get("name", "")
            svc    = inc.get("service", "")
            link   = inc.get("shortlink", "")
            href   = f' href="{link}"' if link else ""
            parts.append(
                f'<a class="outage-item outage-item--active"{href} target="_blank" rel="noopener">'
                f'<span class="outage-dot outage-dot--active"></span>'
                f'<span class="outage-service">{svc}</span>'
                f'<span class="outage-impact impact-{inc.get("impact","")}">{impact}</span>'
                f'<span class="outage-name">{name}</span>'
                f'</a>'
            )
        parts.append('</div></div>')

    # Resolved incidents (last 24h)
    if resolved:
        parts.append(
            '<div class="outage-section">'
            '<div class="section-head"><span class="section-label">Resolved (last 24h)</span>'
            '<div class="section-line"></div></div>'
            '<div class="outage-list">'
        )
        for inc in resolved:
            name = inc.get("name", "")
            svc  = inc.get("service", "")
            link = inc.get("shortlink", "")
            href = f' href="{link}"' if link else ""
            parts.append(
                f'<a class="outage-item outage-item--resolved"{href} target="_blank" rel="noopener">'
                f'<span class="outage-dot outage-dot--resolved"></span>'
                f'<span class="outage-service">{svc}</span>'
                f'<span class="outage-name">{name}</span>'
                f'</a>'
            )
        parts.append('</div></div>')

    parts.append(f'<p class="outage-timestamp">Last updated: {timestamp}</p>')
    return "\n".join(parts)


# ── Service registry ──────────────────────────────────────────────────────────

STATUSPAGE_SERVICES = [
    ("GitHub",        "githubstatus.com",        "devtools"),
    ("npm",           "status.npmjs.org",          "devtools"),
    ("Vercel",        "vercel-status.com",         "devtools"),
    ("Netlify",       "netlifystatus.com",          "devtools"),
    ("Render",        "status.render.com",          "devtools"),
    ("CircleCI",      "status.circleci.com",        "devtools"),
    ("Cloudflare",    "cloudflarestatus.com",        "cdn"),
    ("Akamai",        "status.akamai.com",           "cdn"),
    ("Datadog",       "status.datadoghq.com",        "observability"),
    ("New Relic",     "status.newrelic.com",         "observability"),
    ("Sentry",        "status.sentry.io",            "observability"),
    ("Discord",       "discordstatus.com",           "communication"),
    ("Zoom",          "status.zoom.us",              "communication"),
    ("Twilio",        "status.twilio.com",           "payments"),
    ("MongoDB Atlas", "status.mongodb.com",          "data"),
    ("Snowflake",     "status.snowflake.com",        "data"),
    ("Elastic Cloud", "status.elastic.co",           "data"),
    ("OpenAI",        "status.openai.com",           "ai"),
    ("Anthropic",     "status.anthropic.com",        "ai"),
    ("Atlassian",     "status.atlassian.com",        "saas"),
    ("Notion",        "status.notion.so",            "saas"),
]

# Services with non-standard APIs — fetched individually
SLACK_API = "https://status.slack.com/api/v2.0.0/current"

# Services with no accessible API — shown as static links only
STATIC_SERVICES = [
    ("GitLab",      "https://status.gitlab.com",       "devtools"),
    ("Docker Hub",  "https://status.docker.com",        "devtools"),
    ("Fastly",      "https://fastlystatus.com",          "cdn"),
    ("PagerDuty",   "https://status.pagerduty.com",     "observability"),
    ("Stripe",      "https://status.stripe.com",        "payments"),
    ("Okta",        "https://status.okta.com",          "identity"),
    ("Auth0",       "https://status.auth0.com",         "identity"),
    ("HuggingFace", "https://status.huggingface.co",    "ai"),
    ("Linear",      "https://linear.statuspage.io",     "saas"),
    ("Oracle Cloud","https://ocistatus.oracle.com",     "cloud"),
]

RSS_SERVICES = [
    ("AWS",           "https://status.aws.amazon.com/rss/all.rss",             "cloud"),
    ("Google Cloud",  "https://status.cloud.google.com/en/feed.atom",          "cloud"),
    ("Azure",         "https://azure.status.microsoft/en-us/status/feed/",     "cloud"),
    ("Microsoft 365", "https://status.office365.com/feed/",                    "communication"),
]

_INDICATOR_MAP = {
    "none":        "operational",
    "minor":       "degraded",
    "major":       "outage",
    "critical":    "outage",
    "maintenance": "degraded",
}

FETCH_TIMEOUT = 8
_RSS_INCIDENT_WINDOW_HOURS = 6
_HEADERS = {"User-Agent": "eof.news/1.0 outage-monitor", "Accept": "application/json"}

CATEGORY_ORDER = [
    "cloud", "cdn", "devtools", "observability",
    "communication", "payments", "identity", "data", "ai", "saas",
]

DATA_PATH = os.path.join(os.path.dirname(__file__), "docs", "_data", "outages.json")


# ── Fetchers ──────────────────────────────────────────────────────────────────

def _fetch_statuspage(name: str, domain: str, category: str) -> dict:
    """Fetch summary from one Atlassian Statuspage service."""
    url = f"https://{domain}/api/v2/summary.json"
    try:
        r = requests.get(url, headers=_HEADERS, timeout=FETCH_TIMEOUT)
        r.raise_for_status()
        data = r.json()
    except Exception:
        return {
            "name": name, "domain": domain, "category": category,
            "status": "unknown", "description": "", "incident_url": "", "updated_at": "",
        }

    indicator = data.get("status", {}).get("indicator", "none")
    status = _INDICATOR_MAP.get(indicator, "unknown")

    incidents = data.get("incidents", [])
    active = [i for i in incidents if i.get("resolved_at") is None]
    description  = active[0].get("name", "")       if active else ""
    incident_url = active[0].get("shortlink", "")   if active else ""
    updated_at   = active[0].get("updated_at", "")  if active else ""

    return {
        "name":         name,
        "domain":       domain,
        "category":     category,
        "status":       status,
        "description":  description,
        "incident_url": incident_url,
        "updated_at":   updated_at,
    }


def _fetch_rss(name: str, feed_url: str, category: str) -> dict:
    """Derive status from recency of RSS/Atom entries."""
    try:
        feed = feedparser.parse(feed_url)
        entries = feed.get("entries", [])
    except Exception:
        return {
            "name": name, "domain": feed_url, "category": category,
            "status": "unknown", "description": "", "incident_url": "", "updated_at": "",
        }

    cutoff = datetime.now(timezone.utc) - timedelta(hours=_RSS_INCIDENT_WINDOW_HOURS)
    recent = []
    for entry in entries:
        published = entry.get("published_parsed") or entry.get("updated_parsed")
        if not published:
            continue
        entry_dt = datetime(*published[:6], tzinfo=timezone.utc)
        if entry_dt > cutoff:
            recent.append(entry)

    if not recent:
        return {
            "name": name, "domain": feed_url, "category": category,
            "status": "operational", "description": "", "incident_url": "", "updated_at": "",
        }

    return {
        "name":         name,
        "domain":       feed_url,
        "category":     category,
        "status":       "degraded",
        "description":  recent[0].get("title", ""),
        "incident_url": recent[0].get("link", ""),
        "updated_at":   recent[0].get("updated", ""),
    }


def _fetch_slack() -> dict:
    """Fetch Slack status via its non-standard API."""
    try:
        r = requests.get(SLACK_API, headers=_HEADERS, timeout=FETCH_TIMEOUT)
        r.raise_for_status()
        data = r.json()
    except Exception:
        return {
            "name": "Slack", "domain": "status.slack.com", "category": "communication",
            "status": "unknown", "description": "", "incident_url": "", "updated_at": "",
        }

    active = data.get("active_incidents", [])
    if data.get("status") == "ok" and not active:
        status = "operational"
    else:
        status = "degraded"

    description  = active[0].get("title", "")        if active else ""
    incident_url = active[0].get("url", "")          if active else ""
    updated_at   = active[0].get("date_updated", "") if active else ""

    return {
        "name":         "Slack",
        "domain":       "status.slack.com",
        "category":     "communication",
        "status":       status,
        "description":  description,
        "incident_url": incident_url,
        "updated_at":   updated_at,
    }


def _fetch_hn_community() -> list:
    """Fetch recent HN stories mentioning outage/down in the last 3h."""
    cutoff_ts = int((datetime.now(timezone.utc) - timedelta(hours=3)).timestamp())
    url = (
        "https://hn.algolia.com/api/v1/search"
        "?query=outage+down+incident"
        "&tags=story"
        f"&numericFilters=created_at_i>{cutoff_ts}"
        "&hitsPerPage=8"
    )
    try:
        r = requests.get(url, timeout=FETCH_TIMEOUT)
        r.raise_for_status()
        hits = r.json().get("hits", [])
    except Exception:
        return []

    results = []
    for h in hits:
        created = h.get("created_at_i", 0)
        ago_mins = int((datetime.now(timezone.utc).timestamp() - created) / 60)
        ago = f"{ago_mins}m" if ago_mins < 60 else f"{ago_mins // 60}h"
        results.append({
            "title":  h.get("title", ""),
            "url":    f"https://news.ycombinator.com/item?id={h.get('objectID', '')}",
            "points": h.get("points", 0),
            "ago":    ago,
        })

    results.sort(key=lambda x: x["points"], reverse=True)
    return results


# ── Orchestrator ──────────────────────────────────────────────────────────────

def publish_outages() -> None:
    """Fetch all sources concurrently and write docs/_data/outages.json."""
    print("[outages] Fetching services...")

    all_tasks = (
        [("statuspage", name, domain, category) for name, domain, category in STATUSPAGE_SERVICES]
        + [("rss", name, feed_url, category) for name, feed_url, category in RSS_SERVICES]
        + [("slack", "Slack", SLACK_API, "communication")]
    )

    services = []
    with ThreadPoolExecutor(max_workers=16) as pool:
        futures = {}
        for kind, name, url, category in all_tasks:
            if kind == "statuspage":
                f = pool.submit(_fetch_statuspage, name, url, category)
            elif kind == "rss":
                f = pool.submit(_fetch_rss, name, url, category)
            else:
                f = pool.submit(_fetch_slack)
            futures[f] = name

        for future in as_completed(futures):
            try:
                services.append(future.result())
            except Exception as e:
                print(f"[outages] Error fetching {futures[future]}: {e}")

    # Add static services (no live polling, just links)
    static = [
        {"name": name, "domain": url, "category": cat,
         "status": "static", "description": "", "incident_url": url, "updated_at": ""}
        for name, url, cat in STATIC_SERVICES
    ]

    cat_idx = {c: i for i, c in enumerate(CATEGORY_ORDER)}
    services.sort(key=lambda s: (cat_idx.get(s["category"], 99), s["name"]))
    static.sort(key=lambda s: (cat_idx.get(s["category"], 99), s["name"]))

    now_utc = datetime.now(timezone.utc)
    active = []
    for svc in services:
        if svc["status"] in ("degraded", "outage") and svc["description"] and svc.get("incident_url"):
            active.append({
                "service":     svc["name"],
                "name":        svc["description"],
                "status":      svc["status"],
                "impact":      "major" if svc["status"] == "outage" else "minor",
                "started_at":  svc.get("updated_at", ""),
                "updated_at":  svc.get("updated_at", ""),
                "resolved_at": None,
                "shortlink":   svc.get("incident_url", ""),
            })

    timestamp = now_utc.strftime("%Y-%m-%d %H:%M UTC")
    incidents_html = _generate_page(active, [], timestamp)

    statuses = [s["status"] for s in services]
    summary = {
        "total":       len(services),
        "operational": statuses.count("operational"),
        "degraded":    statuses.count("degraded"),
        "outage":      statuses.count("outage"),
        "unknown":     statuses.count("unknown"),
    }

    community = _fetch_hn_community()

    data = {
        "generated_at":  now_utc.isoformat(),
        "summary":        summary,
        "services":       services,
        "static_services": static,
        "incidents_html": incidents_html,
        "community":      community,
    }

    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[outages] Done - {len(services)} services, {len(active)} active incidents -> {DATA_PATH}")
