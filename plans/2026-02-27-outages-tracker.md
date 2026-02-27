# Outages Tracker Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a `/outages/` page that tracks real-time service incidents for ~20 major developer services, refreshed every 30 minutes via GitHub Actions.

**Architecture:** A new `outages.py` script polls statuspage.io JSON APIs (standard across most services) plus custom endpoints for AWS/GCP/Azure. Results are written to `docs/_data/outages.json`. A static Jekyll page at `docs/outages/index.md` renders the data. A lightweight history file (`docs/_data/outages_history.json`) tracks recently resolved incidents (last 24h) so they appear even after the service recovers.

**Tech Stack:** Python stdlib (`urllib`, `json`, `datetime`), statuspage.io `/api/v2/incidents.json` API, GitHub Actions cron (every 30 min), Jekyll/Liquid for rendering.

---

## Task 1: Write `outages.py` — service definitions and fetch logic

**Files:**
- Create: `outages.py`

### Step 1: Create the file with service definitions and `_fetch_statuspage()`

The statuspage.io API is standard across most services. Endpoint:
`GET https://{domain}/api/v2/incidents.json?limit=10`

Returns `{"incidents": [...]}` where each incident has:
- `id`, `name`, `status` (`investigating` / `identified` / `monitoring` / `resolved`)
- `impact` (`none` / `minor` / `major` / `critical`)
- `started_at`, `resolved_at` (null if not resolved), `updated_at`
- `shortlink`

```python
"""
Service Outage Tracker.
Polls statuspage.io APIs and custom endpoints for major developer services.
Generates docs/_data/outages.json and docs/outages/index.md.
"""
import json
import os
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

DATA_DIR = "docs/_data"
OUTPUT_JSON = os.path.join(DATA_DIR, "outages.json")
HISTORY_JSON = os.path.join(DATA_DIR, "outages_history.json")
OUTPUT_DIR = "docs/outages"
OUTPUT_PAGE = os.path.join(OUTPUT_DIR, "index.md")

# Services using standard statuspage.io API
# Each entry: (display_name, status_page_url, incidents_api_url)
STATUSPAGE_SERVICES = [
    ("GitHub",        "https://www.githubstatus.com",        "https://www.githubstatus.com/api/v2/incidents.json?limit=5"),
    ("Vercel",        "https://www.vercel-status.com",       "https://www.vercel-status.com/api/v2/incidents.json?limit=5"),
    ("Netlify",       "https://www.netlifystatus.com",       "https://www.netlifystatus.com/api/v2/incidents.json?limit=5"),
    ("npm",           "https://status.npmjs.org",            "https://status.npmjs.org/api/v2/incidents.json?limit=5"),
    ("Docker Hub",    "https://status.docker.com",           "https://status.docker.com/api/v2/incidents.json?limit=5"),
    ("Stripe",        "https://status.stripe.com",           "https://status.stripe.com/api/v2/incidents.json?limit=5"),
    ("Cloudflare",    "https://www.cloudflarestatus.com",    "https://www.cloudflarestatus.com/api/v2/incidents.json?limit=5"),
    ("Datadog",       "https://status.datadoghq.com",        "https://status.datadoghq.com/api/v2/incidents.json?limit=5"),
    ("PagerDuty",     "https://status.pagerduty.com",        "https://status.pagerduty.com/api/v2/incidents.json?limit=5"),
    ("Auth0",         "https://status.auth0.com",            "https://status.auth0.com/api/v2/incidents.json?limit=5"),
    ("Okta",          "https://status.okta.com",             "https://status.okta.com/api/v2/incidents.json?limit=5"),
    ("SendGrid",      "https://status.sendgrid.com",         "https://status.sendgrid.com/api/v2/incidents.json?limit=5"),
    ("MongoDB Atlas", "https://status.mongodb.com",          "https://status.mongodb.com/api/v2/incidents.json?limit=5"),
    ("Slack",         "https://status.slack.com",            "https://status.slack.com/api/v2/incidents.json?limit=5"),
    ("Heroku",        "https://status.heroku.com",           "https://status.heroku.com/api/v2/incidents.json?limit=5"),
    ("CircleCI",      "https://status.circleci.com",         "https://status.circleci.com/api/v2/incidents.json?limit=5"),
    ("Fastly",        "https://www.fastlystatus.com",        "https://www.fastlystatus.com/api/v2/incidents.json?limit=5"),
    ("Twilio",        "https://status.twilio.com",           "https://status.twilio.com/api/v2/incidents.json?limit=5"),
    ("Sentry",        "https://status.sentry.io",            "https://status.sentry.io/api/v2/incidents.json?limit=5"),
    ("Supabase",      "https://status.supabase.com",         "https://status.supabase.com/api/v2/incidents.json?limit=5"),
    ("AWS",           "https://health.aws.amazon.com/health/status", "https://health.aws.amazon.com/health/status"),
    ("GCP",           "https://status.cloud.google.com",    "https://status.cloud.google.com/incidents.json"),
    ("Azure",         "https://status.azure.com",            None),  # RSS-only, handled separately
]

IMPACT_ORDER = {"critical": 0, "major": 1, "minor": 2, "none": 3, "": 4}


def _fetch_statuspage(name, api_url, status_url):
    """Fetch incidents from a statuspage.io-compatible endpoint."""
    headers = {"User-Agent": "eof.news Outage Tracker"}
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data.get("incidents", [])
    except Exception as e:
        print(f"  [{name}] fetch error: {e}")
        return []
```

### Step 2: Add `_parse_incident()` helper

```python
def _parse_incident(raw, service_name):
    """Normalize a statuspage.io incident dict."""
    return {
        "id": raw.get("id", ""),
        "name": raw.get("name", "Unknown incident"),
        "status": raw.get("status", ""),
        "impact": raw.get("impact", ""),
        "started_at": raw.get("created_at") or raw.get("started_at", ""),
        "resolved_at": raw.get("resolved_at"),
        "updated_at": raw.get("updated_at", ""),
        "shortlink": raw.get("shortlink", ""),
        "service": service_name,
    }
```

### Step 3: Add GCP fetcher

GCP uses `https://status.cloud.google.com/incidents.json` which returns a list of incident objects directly (not wrapped in `{"incidents": ...}`).

```python
def _fetch_gcp():
    """Fetch GCP incidents from their custom JSON feed."""
    url = "https://status.cloud.google.com/incidents.json"
    headers = {"User-Agent": "eof.news Outage Tracker"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        # GCP format: list of {id, service_name, external_desc, status_impact, begin, end, ...}
        incidents = []
        for raw in data[:5]:
            end = raw.get("end")
            resolved_at = end if end else None
            status = "resolved" if resolved_at else "investigating"
            impact_map = {
                "SERVICE_DISRUPTION": "major",
                "SERVICE_INFORMATION": "minor",
                "SERVICE_OUTAGE": "critical",
            }
            impact = impact_map.get(raw.get("status_impact", ""), "minor")
            incidents.append({
                "id": raw.get("id", ""),
                "name": raw.get("external_desc", "GCP Incident"),
                "status": status,
                "impact": impact,
                "started_at": raw.get("begin", ""),
                "resolved_at": resolved_at,
                "updated_at": raw.get("modified", ""),
                "shortlink": f"https://status.cloud.google.com/incidents/{raw.get('id', '')}",
                "service": "GCP",
            })
        return incidents
    except Exception as e:
        print(f"  [GCP] fetch error: {e}")
        return []
```

### Step 4: Add `_is_recent_resolved()` and `_collect_all_incidents()`

```python
def _is_recent_resolved(incident, hours=24):
    """Return True if incident was resolved within the last N hours."""
    resolved_at = incident.get("resolved_at")
    if not resolved_at:
        return False
    try:
        resolved_dt = datetime.fromisoformat(resolved_at.replace("Z", "+00:00"))
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        return resolved_dt >= cutoff
    except (ValueError, AttributeError):
        return False


def _collect_all_incidents():
    """Fetch all services. Returns (active_incidents, recent_resolved)."""
    all_active = []
    all_resolved = []

    for name, status_url, api_url in STATUSPAGE_SERVICES:
        if name == "GCP":
            incidents = _fetch_gcp()
        elif name in ("AWS", "Azure") or api_url is None:
            # Skip for v1 — link to status page directly
            print(f"  [{name}] skipped (custom format)")
            continue
        else:
            raw_list = _fetch_statuspage(name, api_url, status_url)
            incidents = [_parse_incident(r, name) for r in raw_list]

        for inc in incidents:
            if inc["status"] == "resolved":
                if _is_recent_resolved(inc):
                    all_resolved.append(inc)
            else:
                all_active.append(inc)

        active_count = sum(1 for i in incidents if i["status"] != "resolved")
        print(f"  [{name}] {active_count} active incidents")

    # Sort: active by impact severity, resolved by resolved_at desc
    all_active.sort(key=lambda i: IMPACT_ORDER.get(i["impact"], 4))
    all_resolved.sort(key=lambda i: i.get("resolved_at") or "", reverse=True)

    return all_active, all_resolved
```

---

## Task 2: Write `outages.py` — JSON output and page generation

**Files:**
- Modify: `outages.py` (continue)

### Step 1: Add `_write_json()`

```python
def _write_json(active, resolved):
    """Write outages.json with active + recently resolved incidents."""
    now = datetime.now(timezone.utc)
    output = {
        "generated_at": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "active_count": len(active),
        "resolved_count": len(resolved),
        "active": active,
        "resolved_24h": resolved,
    }
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"  JSON written: {OUTPUT_JSON}")
```

### Step 2: Add `_generate_page()`

The page has three states:
1. Active incidents — red/orange cards
2. Recently resolved (last 24h) — grey cards
3. All clear — green banner

```python
def _generate_page(active, resolved, generated_at):
    """Generate Jekyll markdown page for /outages/."""

    def _impact_color(impact):
        return {
            "critical": "#b91c1c",
            "major": "#dc2626",
            "minor": "#ca8a04",
            "none": "#6b7280",
        }.get(impact, "#6b7280")

    def _status_label(status):
        return {
            "investigating": "🔴 Investigating",
            "identified": "🟠 Identified",
            "monitoring": "🟡 Monitoring",
            "resolved": "✅ Resolved",
        }.get(status, status.title())

    def _format_dt(dt_str):
        if not dt_str:
            return ""
        try:
            dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
            return dt.strftime("%b %d, %H:%M UTC")
        except (ValueError, AttributeError):
            return dt_str[:16]

    lines = [
        "---",
        'layout: page',
        'title: "Service Outages"',
        'description: "Real-time outage tracker for major developer services. GitHub, AWS, GCP, Cloudflare, Stripe, and more."',
        "permalink: /outages/",
        "---",
        "",
    ]

    if not active and not resolved:
        lines += [
            '<div style="padding:1.5em; border:2px solid #16a34a; border-radius:8px; background:#f0fdf4; margin-bottom:1.5em;">',
            '  <strong style="color:#15803d; font-size:1.1em;">✅ All systems operational</strong>',
            '  <p style="margin:0.5em 0 0 0; color:#166534;">No active incidents detected across tracked services.</p>',
            '</div>',
            "",
        ]
    else:
        if active:
            lines += [
                f'<div style="padding:0.75em 1em; border-radius:8px; background:#fef2f2; border:1px solid #fca5a5; margin-bottom:1.5em;">',
                f'  <strong style="color:#b91c1c;">⚠ {len(active)} active incident{"s" if len(active) != 1 else ""}</strong>',
                '</div>',
                "",
                "## Active Incidents",
                "",
            ]
            for inc in active:
                color = _impact_color(inc["impact"])
                lines += [
                    f'<div style="margin-bottom:1em; padding:1em; border-left:4px solid {color}; border-radius:0 8px 8px 0; background:#fafafa;">',
                    f'  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap; margin-bottom:0.4em;">',
                    f'    <strong style="font-size:1em;">{inc["service"]}</strong>',
                    f'    <span style="padding:2px 8px; border-radius:12px; font-size:0.78em; background:{color}; color:#fff;">{inc["impact"].upper()}</span>',
                    f'    <span style="font-size:0.82em; color:#6b7280;">{_status_label(inc["status"])}</span>',
                    f'  </div>',
                    f'  <div style="font-weight:600; margin-bottom:0.25em;">',
                ]
                if inc.get("shortlink"):
                    lines.append(f'    <a href="{inc["shortlink"]}" target="_blank" rel="noopener" style="color:#111;">{inc["name"]}</a>')
                else:
                    lines.append(f'    {inc["name"]}')
                lines += [
                    f'  </div>',
                    f'  <div style="font-size:0.82em; color:#6b7280;">',
                    f'    Started: {_format_dt(inc["started_at"])}',
                    f'    &nbsp;·&nbsp; Updated: {_format_dt(inc["updated_at"])}',
                    f'  </div>',
                    '</div>',
                    "",
                ]

    if resolved:
        lines += [
            "## Resolved (last 24h)",
            "",
        ]
        for inc in resolved:
            lines += [
                f'<div style="margin-bottom:0.75em; padding:0.75em 1em; border-left:4px solid #d1d5db; border-radius:0 8px 8px 0; background:#f9fafb; opacity:0.8;">',
                f'  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap;">',
                f'    <strong style="color:#374151;">{inc["service"]}</strong>',
                f'    <span style="font-size:0.78em; color:#6b7280;">✅ Resolved</span>',
                f'    <span style="font-size:0.82em; color:#9ca3af;">{inc["name"]}</span>',
                f'    <span style="font-size:0.78em; color:#9ca3af;">· {_format_dt(inc.get("resolved_at", ""))}</span>',
                f'  </div>',
                '</div>',
                "",
            ]

    lines += [
        "---",
        "",
        f'<p style="font-size:0.8em; color:#9ca3af;">Updated: {generated_at} &middot; Checks every 30 minutes</p>',
        "",
    ]

    return "\n".join(lines)
```

### Step 3: Add `publish_outages()` entry point

```python
def publish_outages():
    """Main entry point."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Fetching service status...")
    active, resolved = _collect_all_incidents()

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"Active: {len(active)}, Resolved 24h: {len(resolved)}")

    _write_json(active, resolved)

    page = _generate_page(active, resolved, now_str)
    with open(OUTPUT_PAGE, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"  Page written: {OUTPUT_PAGE}")
```

---

## Task 3: Write tests for `outages.py`

**Files:**
- Create: `tests/test_outages.py`

### Step 1: Write tests

```python
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta
from outages import _parse_incident, _is_recent_resolved, _impact_color_exists, _format_dt_valid


def test_parse_incident_maps_fields():
    raw = {
        "id": "abc123",
        "name": "API is down",
        "status": "investigating",
        "impact": "critical",
        "created_at": "2026-02-27T09:00:00Z",
        "resolved_at": None,
        "updated_at": "2026-02-27T09:15:00Z",
        "shortlink": "https://stspg.io/abc123",
    }
    result = _parse_incident(raw, "GitHub")
    assert result["id"] == "abc123"
    assert result["name"] == "API is down"
    assert result["status"] == "investigating"
    assert result["impact"] == "critical"
    assert result["service"] == "GitHub"
    assert result["resolved_at"] is None


def test_is_recent_resolved_within_24h():
    recent = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
    inc = {"resolved_at": recent, "status": "resolved"}
    assert _is_recent_resolved(inc) is True


def test_is_recent_resolved_older_than_24h():
    old = (datetime.now(timezone.utc) - timedelta(hours=25)).isoformat()
    inc = {"resolved_at": old, "status": "resolved"}
    assert _is_recent_resolved(inc) is False


def test_is_recent_resolved_no_resolved_at():
    inc = {"resolved_at": None, "status": "investigating"}
    assert _is_recent_resolved(inc) is False
```

Note: `_impact_color_exists` and `_format_dt_valid` are internal to `_generate_page` — test those by calling `_generate_page` directly with known data.

```python
from outages import _generate_page


def test_generate_page_all_clear():
    page = _generate_page([], [], "2026-02-27 10:00:00 UTC")
    assert "All systems operational" in page
    assert "Active Incidents" not in page


def test_generate_page_active_incident():
    active = [{
        "service": "GitHub",
        "name": "API slowness",
        "status": "investigating",
        "impact": "critical",
        "started_at": "2026-02-27T09:00:00Z",
        "updated_at": "2026-02-27T09:15:00Z",
        "resolved_at": None,
        "shortlink": "https://stspg.io/x",
    }]
    page = _generate_page(active, [], "2026-02-27 10:00:00 UTC")
    assert "Active Incidents" in page
    assert "GitHub" in page
    assert "CRITICAL" in page
    assert "All systems operational" not in page


def test_generate_page_resolved_only():
    resolved = [{
        "service": "Stripe",
        "name": "Payments degraded",
        "status": "resolved",
        "impact": "major",
        "started_at": "2026-02-27T06:00:00Z",
        "updated_at": "2026-02-27T08:00:00Z",
        "resolved_at": "2026-02-27T08:30:00Z",
        "shortlink": "",
    }]
    page = _generate_page([], resolved, "2026-02-27 10:00:00 UTC")
    assert "Resolved (last 24h)" in page
    assert "Stripe" in page
```

### Step 2: Run tests

```bash
cd /c/repo/ipsedigit.github.io
python -m pytest tests/test_outages.py -v
```

Expected: all pass.

---

## Task 4: Wire into `main.py` and add nav item

**Files:**
- Modify: `main.py`
- Modify: `docs/_includes/header.html`

### Step 1: Add `outages` case to `main.py`

In `main.py`, add after the `"github"` case:

```python
        case "outages":
            from outages import publish_outages
            publish_outages()
```

Also update the `--action` help string to include `outages`.

### Step 2: Add "Outages" to header nav

In `docs/_includes/header.html`, the current nav order is:
`Home → GitHub → Models → Bootleg → CVEs`

Add Outages before CVEs:

```html
        <a class="nav-item" href="/outages/">Outages</a>
        <a class="nav-item" href="/security/cves/">CVEs</a>
```

---

## Task 5: Create GitHub Actions workflow

**Files:**
- Create: `.github/workflows/outagestracker.yml`

### Step 1: Write the workflow

```yaml
name: Outages Tracker

on:
  schedule:
    - cron: '*/30 5-21 * * *'   # every 30 min, 06:00-22:00 Rome (UTC+1)
  workflow_dispatch:

jobs:
  run-outages:
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

    - name: Run Outages Tracker
      run: python main.py --action=outages

    - name: Commit and Push changes
      run: |
        find . -type d -name "__pycache__" -exec rm -r {} +
        find . -name "*.pyc" -delete
        git add .
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
        git commit -m "Auto: outages update at $TIMESTAMP" || echo "No changes to commit"
        git push origin main
```

### Step 2: Verify the workflow triggers

After committing, go to GitHub Actions → "Outages Tracker" → Run workflow (manual trigger) to verify it runs without errors.

---

## Task 6: Create `docs/outages/` directory placeholder

**Files:**
- Create: `docs/outages/.gitkeep`

The directory must exist before the first script run. The script creates it with `os.makedirs(..., exist_ok=True)` but git doesn't track empty dirs.

```bash
touch docs/outages/.gitkeep
```

---

## Summary

| File | Action |
|------|--------|
| `outages.py` | Create — fetch + generate |
| `tests/test_outages.py` | Create — unit tests |
| `main.py` | Modify — add `outages` case |
| `docs/_includes/header.html` | Modify — add nav item |
| `.github/workflows/outagestracker.yml` | Create — 30-min schedule |
| `docs/outages/.gitkeep` | Create — dir placeholder |
