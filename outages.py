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
OUTPUT_DIR = "docs/outages"
OUTPUT_PAGE = os.path.join(OUTPUT_DIR, "index.md")

# (display_name, status_page_url, incidents_api_url)
# api_url="gcp" means custom GCP handler; None means skipped
SERVICES = [
    ("GitHub",        "https://www.githubstatus.com",        "https://www.githubstatus.com/api/v2/incidents.json"),
    ("Vercel",        "https://www.vercel-status.com",       "https://www.vercel-status.com/api/v2/incidents.json"),
    ("Netlify",       "https://www.netlifystatus.com",       "https://www.netlifystatus.com/api/v2/incidents.json"),
    ("npm",           "https://status.npmjs.org",            "https://status.npmjs.org/api/v2/incidents.json"),
    ("Cloudflare",    "https://www.cloudflarestatus.com",    "https://www.cloudflarestatus.com/api/v2/incidents.json"),
    ("Datadog",       "https://status.datadoghq.com",        "https://status.datadoghq.com/api/v2/incidents.json"),
    ("SendGrid",      "https://status.sendgrid.com",         "https://status.sendgrid.com/api/v2/incidents.json"),
    ("MongoDB Atlas", "https://status.mongodb.com",          "https://status.mongodb.com/api/v2/incidents.json"),
    ("CircleCI",      "https://status.circleci.com",         "https://status.circleci.com/api/v2/incidents.json"),
    ("Twilio",        "https://status.twilio.com",           "https://status.twilio.com/api/v2/incidents.json"),
    ("Sentry",        "https://status.sentry.io",            "https://status.sentry.io/api/v2/incidents.json"),
    ("Supabase",      "https://status.supabase.com",         "https://status.supabase.com/api/v2/incidents.json"),
    ("GCP",           "https://status.cloud.google.com",     "gcp"),
]

IMPACT_ORDER = {"critical": 0, "major": 1, "minor": 2, "none": 3, "": 4}


def _fetch_statuspage(name, api_url):
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


def _fetch_gcp():
    """Fetch GCP incidents from their custom JSON feed."""
    url = "https://status.cloud.google.com/incidents.json"
    headers = {"User-Agent": "eof.news Outage Tracker"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        impact_map = {
            "SERVICE_DISRUPTION": "major",
            "SERVICE_INFORMATION": "minor",
            "SERVICE_OUTAGE": "critical",
        }
        incidents = []
        for raw in data[:5]:
            end = raw.get("end")
            incidents.append({
                "id": raw.get("id", ""),
                "name": raw.get("external_desc", "GCP Incident"),
                "status": "resolved" if end else "investigating",
                "impact": impact_map.get(raw.get("status_impact", ""), "minor"),
                "started_at": raw.get("begin", ""),
                "resolved_at": end if end else None,
                "updated_at": raw.get("modified", ""),
                "shortlink": f"https://status.cloud.google.com/incidents/{raw.get('id', '')}",
                "service": "GCP",
            })
        return incidents
    except Exception as e:
        print(f"  [GCP] fetch error: {e}")
        return []


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


def _is_stale_active(incident, days=7):
    """Return True if a non-resolved incident hasn't been updated in N days (stale monitoring)."""
    updated_at = incident.get("updated_at") or incident.get("started_at", "")
    if not updated_at:
        return True
    try:
        updated_dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        return updated_dt < cutoff
    except (ValueError, AttributeError):
        return True


def _collect_all_incidents():
    """Fetch all services. Returns (active_incidents, recent_resolved)."""
    all_active = []
    all_resolved = []

    for name, status_url, api_url in SERVICES:
        if api_url is None:
            print(f"  [{name}] skipped (custom format — link: {status_url})")
            continue
        elif api_url == "gcp":
            incidents = _fetch_gcp()
        else:
            raw_list = _fetch_statuspage(name, api_url)
            incidents = [_parse_incident(r, name) for r in raw_list]

        for inc in incidents:
            if inc["status"] in ("resolved", "postmortem"):
                if _is_recent_resolved(inc):
                    all_resolved.append(inc)
            elif not _is_stale_active(inc):
                all_active.append(inc)

        active_count = sum(1 for i in incidents if i["status"] != "resolved")
        print(f"  [{name}] {active_count} active incidents")

    all_active.sort(key=lambda i: IMPACT_ORDER.get(i["impact"], 4))
    all_resolved.sort(key=lambda i: i.get("resolved_at") or "", reverse=True)

    return all_active, all_resolved


def _write_json(active, resolved, generated_at):
    """Write outages.json."""
    output = {
        "generated_at": generated_at,
        "active_count": len(active),
        "resolved_count": len(resolved),
        "active": active,
        "resolved_24h": resolved,
    }
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"  JSON written: {OUTPUT_JSON}")


def _format_dt(dt_str):
    if not dt_str:
        return ""
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%b %d, %H:%M UTC")
    except (ValueError, AttributeError):
        return str(dt_str)[:16]


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


def _generate_page(active, resolved, generated_at):
    """Generate Jekyll markdown page for /outages/."""
    lines = [
        "---",
        "layout: page",
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
                name_html = (
                    f'<a href="{inc["shortlink"]}" target="_blank" rel="noopener" style="color:#111;">{inc["name"]}</a>'
                    if inc.get("shortlink") else inc["name"]
                )
                lines += [
                    f'<div style="margin-bottom:1em; padding:1em; border-left:4px solid {color}; border-radius:0 8px 8px 0; background:#fafafa;">',
                    f'  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap; margin-bottom:0.4em;">',
                    f'    <strong>{inc["service"]}</strong>',
                    f'    <span style="padding:2px 8px; border-radius:12px; font-size:0.78em; background:{color}; color:#fff;">{inc["impact"].upper()}</span>',
                    f'    <span style="font-size:0.82em; color:#6b7280;">{_status_label(inc["status"])}</span>',
                    f'  </div>',
                    f'  <div style="font-weight:600; margin-bottom:0.25em;">{name_html}</div>',
                    f'  <div style="font-size:0.82em; color:#6b7280;">',
                    f'    Started: {_format_dt(inc["started_at"])} &nbsp;·&nbsp; Updated: {_format_dt(inc["updated_at"])}',
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
                '<div style="margin-bottom:0.75em; padding:0.75em 1em; border-left:4px solid #d1d5db; border-radius:0 8px 8px 0; background:#f9fafb; opacity:0.8;">',
                '  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap;">',
                f'    <strong style="color:#374151;">{inc["service"]}</strong>',
                f'    <span style="font-size:0.78em; color:#6b7280;">✅ Resolved {_format_dt(inc.get("resolved_at", ""))}</span>',
                f'    <span style="font-size:0.82em; color:#9ca3af;">{inc["name"]}</span>',
                '  </div>',
                '</div>',
                "",
            ]

    lines += [
        "---",
        "",
        f'<p style="font-size:0.8em; color:#9ca3af;">Data from statuspage.io APIs &middot; Updated: {generated_at}</p>',
        "",
    ]

    return "\n".join(lines)


def publish_outages():
    """Main entry point."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Fetching service status...")
    active, resolved = _collect_all_incidents()

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"Active: {len(active)}, Resolved 24h: {len(resolved)}")

    _write_json(active, resolved, now_str)

    page = _generate_page(active, resolved, now_str)
    with open(OUTPUT_PAGE, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"  Page written: {OUTPUT_PAGE}")
