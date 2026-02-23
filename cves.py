"""
CVE Tracker.
Fetches recent CVEs from NVD API, cross-references with site posts,
and generates docs/_data/cves.json and docs/security/cves.md.
"""
import json
import os
import re
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta

from post_parser import get_recent_posts

DATA_DIR = "docs/_data"
OUTPUT_JSON = os.path.join(DATA_DIR, "cves.json")
OUTPUT_DIR = "docs/security"
OUTPUT_PAGE = os.path.join(OUTPUT_DIR, "cves.md")

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def _fetch_recent_cves(days=3, max_results=50):
    """Fetch recent CVEs from NVD API (free, no key required)."""
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=days)

    params = {
        "pubStartDate": start.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "pubEndDate": now.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "resultsPerPage": str(max_results),
    }

    url = f"{NVD_API_URL}?{urllib.parse.urlencode(params)}"
    print(f"Fetching CVEs from NVD: {url}")

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "eof.news CVE Tracker"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"⚠️ NVD API error: {e}")
        return []

    cves = []
    for item in data.get("vulnerabilities", []):
        cve_data = item.get("cve", {})
        cve_id = cve_data.get("id", "")

        # Description (English)
        descriptions = cve_data.get("descriptions", [])
        description = ""
        for desc in descriptions:
            if desc.get("lang") == "en":
                description = desc.get("value", "")
                break
        if not description and descriptions:
            description = descriptions[0].get("value", "")

        # CVSS metrics
        metrics = cve_data.get("metrics", {})
        severity = "UNKNOWN"
        score = 0.0

        # Try CVSS 3.1 first, then 3.0, then 2.0
        for version_key in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
            metric_list = metrics.get(version_key, [])
            if metric_list:
                cvss = metric_list[0].get("cvssData", {})
                score = cvss.get("baseScore", 0.0)
                severity = cvss.get("baseSeverity", "UNKNOWN")
                if not severity or severity == "UNKNOWN":
                    # Derive from score
                    if score >= 9.0:
                        severity = "CRITICAL"
                    elif score >= 7.0:
                        severity = "HIGH"
                    elif score >= 4.0:
                        severity = "MEDIUM"
                    elif score > 0:
                        severity = "LOW"
                break

        # Affected products (CPE)
        products = set()
        configurations = cve_data.get("configurations", [])
        for config in configurations:
            for node in config.get("nodes", []):
                for match in node.get("cpeMatch", []):
                    cpe = match.get("criteria", "")
                    # CPE format: cpe:2.3:a:vendor:product:version:...
                    parts = cpe.split(":")
                    if len(parts) >= 5:
                        vendor = parts[3]
                        product = parts[4]
                        if vendor != "*" and product != "*":
                            products.add(f"{vendor}/{product}")

        cves.append({
            "id": cve_id,
            "description": description[:300],
            "severity": severity.upper(),
            "score": score,
            "products": list(products)[:10],
            "published": cve_data.get("published", ""),
            "nvd_url": f"https://nvd.nist.gov/vuln/detail/{cve_id}",
        })

    return cves


def _cross_reference(cves, posts):
    """Find related site posts for each CVE."""
    for cve in cves:
        related = []
        cve_id_lower = cve['id'].lower()
        product_names = [p.split('/')[-1].lower() for p in cve['products']]

        for post in posts:
            text = f"{post['title']} {' '.join(post['categories'])}".lower()
            body = post.get('_body', '').lower()

            # Check if CVE ID mentioned
            if cve_id_lower in text or cve_id_lower in body:
                related.append({"title": post['title'], "url": post['url']})
                continue

            # Check product name match in security posts
            if post['niche_category'] == 'security':
                for prod in product_names:
                    if len(prod) > 2 and prod in text:
                        related.append({"title": post['title'], "url": post['url']})
                        break

        cve['related_posts'] = related[:3]

    return cves


def _generate_page():
    """Generate the Jekyll markdown page for CVE tracker."""
    lines = [
        "---",
        "layout: page",
        'title: "CVE Tracker"',
        'description: "Latest security vulnerabilities tracked daily. Critical, high, medium, and low severity CVEs with cross-references to eof.news coverage."',
        "permalink: /security/cves/",
        "---",
        "",
        "## Vulnerability Summary",
        "",
        "{% assign critical = 0 %}{% assign high = 0 %}{% assign medium = 0 %}{% assign low = 0 %}",
        "{% for cve in site.data.cves.cves %}",
        '  {% if cve.severity == "CRITICAL" %}{% assign critical = critical | plus: 1 %}',
        '  {% elsif cve.severity == "HIGH" %}{% assign high = high | plus: 1 %}',
        '  {% elsif cve.severity == "MEDIUM" %}{% assign medium = medium | plus: 1 %}',
        '  {% elsif cve.severity == "LOW" %}{% assign low = low | plus: 1 %}',
        "  {% endif %}",
        "{% endfor %}",
        "",
        '<div style="display:flex; gap:1em; flex-wrap:wrap; margin-bottom:1.5em;">',
        '  <span style="padding:4px 12px; border-radius:12px; background:#dc2626; color:#fff; font-weight:bold;">CRITICAL: {{ critical }}</span>',
        '  <span style="padding:4px 12px; border-radius:12px; background:#ea580c; color:#fff; font-weight:bold;">HIGH: {{ high }}</span>',
        '  <span style="padding:4px 12px; border-radius:12px; background:#ca8a04; color:#fff; font-weight:bold;">MEDIUM: {{ medium }}</span>',
        '  <span style="padding:4px 12px; border-radius:12px; background:#6b7280; color:#fff; font-weight:bold;">LOW: {{ low }}</span>',
        "</div>",
        "",
        "## Recent CVEs",
        "",
        "{% if site.data.cves.cves.size > 0 %}",
        "{% for cve in site.data.cves.cves %}",
        '<div style="margin-bottom:1.5em; padding:0.75em; border-left:4px solid {% if cve.severity == \'CRITICAL\' %}#dc2626{% elsif cve.severity == \'HIGH\' %}#ea580c{% elsif cve.severity == \'MEDIUM\' %}#ca8a04{% else %}#6b7280{% endif %}; background:#f9fafb;">',
        '  <strong><a href="{{ cve.nvd_url }}">{{ cve.id }}</a></strong>',
        '  <span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.8em; margin-left:0.5em; color:#fff; background:{% if cve.severity == \'CRITICAL\' %}#dc2626{% elsif cve.severity == \'HIGH\' %}#ea580c{% elsif cve.severity == \'MEDIUM\' %}#ca8a04{% else %}#6b7280{% endif %};">{{ cve.severity }} {{ cve.score }}</span>',
        "  <br>",
        '  <span style="font-size:0.9em;">{{ cve.description }}</span>',
        "  {% if cve.products.size > 0 %}",
        '  <br><span style="font-size:0.8em; color:#6b7280;">Products: {{ cve.products | join: ", " }}</span>',
        "  {% endif %}",
        "  {% if cve.related_posts.size > 0 %}",
        '  <br><span style="font-size:0.8em;">Related: ',
        "  {% for rp in cve.related_posts %}",
        '    <a href="{{ rp.url }}">{{ rp.title | truncate: 50 }}</a>{% unless forloop.last %}, {% endunless %}',
        "  {% endfor %}",
        "  </span>",
        "  {% endif %}",
        "</div>",
        "{% endfor %}",
        "{% else %}",
        "<p>No CVEs tracked yet. Check back after the next update.</p>",
        "{% endif %}",
        "",
        "---",
        "",
        '<p style="font-size:0.8em; color:#9ca3af;">',
        "Data from <a href=\"https://nvd.nist.gov/\">NVD</a> &middot; Updated: {{ site.data.cves.generated_at }}",
        "</p>",
        "",
    ]
    return "\n".join(lines)


def publish_cves():
    """Main entry point: fetch CVEs, cross-reference, write JSON and page."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    cves = _fetch_recent_cves(days=3, max_results=50)
    print(f"Fetched {len(cves)} CVEs from NVD")

    # Cross-reference with site posts (last 30 days of security posts)
    posts = get_recent_posts(days=30, niche_filter={'security'})
    cves = _cross_reference(cves, posts)

    # Sort by severity then score
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "UNKNOWN": 4}
    cves.sort(key=lambda c: (severity_order.get(c['severity'], 5), -c['score']))

    now = datetime.now(timezone.utc)
    output = {
        "generated_at": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "total": len(cves),
        "cves": cves,
    }

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"✅ CVE JSON written: {OUTPUT_JSON}")

    page_content = _generate_page()
    with open(OUTPUT_PAGE, 'w', encoding='utf-8') as f:
        f.write(page_content)
    print(f"✅ CVE page written: {OUTPUT_PAGE}")
