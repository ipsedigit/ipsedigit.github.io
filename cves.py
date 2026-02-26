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
CVE_PAGES_DIR = os.path.join(OUTPUT_DIR, "cves")

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
EPSS_API_URL = "https://api.first.org/data/v1/epss"


def _fetch_cisa_kev():
    """Fetch CISA Known Exploited Vulnerabilities catalog. Returns dict CVE-ID → record."""
    print("Fetching CISA KEV catalog...")
    try:
        req = urllib.request.Request(CISA_KEV_URL, headers={"User-Agent": "eof.news CVE Tracker"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"⚠️ CISA KEV fetch error: {e}")
        return {}

    kev = {}
    for vuln in data.get("vulnerabilities", []):
        cve_id = vuln.get("cveID", "")
        if cve_id:
            kev[cve_id] = {
                "date_added": vuln.get("dateAdded", ""),
                "due_date": vuln.get("dueDate", ""),
                "notes": vuln.get("shortDescription", ""),
                "required_action": vuln.get("requiredAction", ""),
            }
    print(f"  CISA KEV: {len(kev)} known exploited vulnerabilities loaded")
    return kev


def _fetch_epss(cve_ids):
    """Fetch EPSS scores in batch. Returns dict CVE-ID → {epss_score, percentile}."""
    if not cve_ids:
        return {}

    print(f"Fetching EPSS scores for {len(cve_ids)} CVEs...")
    try:
        url = f"{EPSS_API_URL}?cve={','.join(cve_ids)}"
        req = urllib.request.Request(url, headers={"User-Agent": "eof.news CVE Tracker"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"⚠️ EPSS fetch error: {e}")
        return {}

    epss = {}
    for entry in data.get("data", []):
        cve_id = entry.get("cve", "")
        if cve_id:
            epss[cve_id] = {
                "epss_score": float(entry.get("epss", 0)),
                "percentile": round(float(entry.get("percentile", 0)) * 100, 1),
            }
    print(f"  EPSS: scores retrieved for {len(epss)} CVEs")
    return epss


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

        # Filter out old CVEs registered late on NVD (e.g. CVE-2019-* published in 2026)
        # Only keep CVEs from current year or previous year
        cve_year_match = re.match(r'CVE-(\d{4})-', cve_id)
        if cve_year_match:
            cve_year = int(cve_year_match.group(1))
            current_year = now.year
            if cve_year < current_year - 1:
                continue

        cves.append({
            "id": cve_id,
            "description": description[:300],
            "full_description": description,
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


def _pick_featured_cve(cves):
    """Select the most critical CVE to spotlight: CISA KEV > severity > EPSS > recency."""
    if not cves:
        return None
    severity_weight = {"CRITICAL": 40, "HIGH": 30, "MEDIUM": 20, "LOW": 10, "UNKNOWN": 0}

    def score(c):
        s = severity_weight.get(c['severity'], 0)
        s += 100 if c.get('cisa_kev') else 0
        s += c.get('epss_score', 0) * 20
        return (s, c.get('published') or '')

    return max(cves, key=score)


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
        "{% assign critical = 0 %}{% assign high = 0 %}{% assign medium = 0 %}{% assign low = 0 %}{% assign exploited = 0 %}",
        "{% for cve in site.data.cves.cves %}",
        '  {% if cve.severity == "CRITICAL" %}{% assign critical = critical | plus: 1 %}',
        '  {% elsif cve.severity == "HIGH" %}{% assign high = high | plus: 1 %}',
        '  {% elsif cve.severity == "MEDIUM" %}{% assign medium = medium | plus: 1 %}',
        '  {% elsif cve.severity == "LOW" %}{% assign low = low | plus: 1 %}',
        "  {% endif %}",
        "  {% if cve.cisa_kev %}{% assign exploited = exploited | plus: 1 %}{% endif %}",
        "{% endfor %}",
        "",
        '<div style="display:flex; gap:1em; flex-wrap:wrap; margin-bottom:1.5em;">',
        '  {% if exploited > 0 %}<span style="padding:4px 12px; border-radius:12px; background:#b91c1c; color:#fff; font-weight:bold;">⚠ EXPLOITED: {{ exploited }}</span>{% endif %}',
        '  <span style="padding:4px 12px; border-radius:12px; background:#dc2626; color:#fff; font-weight:bold;">CRITICAL: {{ critical }}</span>',
        '  <span style="padding:4px 12px; border-radius:12px; background:#ea580c; color:#fff; font-weight:bold;">HIGH: {{ high }}</span>',
        '  <span style="padding:4px 12px; border-radius:12px; background:#ca8a04; color:#fff; font-weight:bold;">MEDIUM: {{ medium }}</span>',
        '  <span style="padding:4px 12px; border-radius:12px; background:#6b7280; color:#fff; font-weight:bold;">LOW: {{ low }}</span>',
        "</div>",
        "",
        "{% if site.data.cves.featured_cve %}",
        "{% assign f = site.data.cves.featured_cve %}",
        "{% assign f_border = '#dc2626' %}",
        "{% if f.severity == 'HIGH' %}{% assign f_border = '#ea580c' %}{% elsif f.severity == 'MEDIUM' %}{% assign f_border = '#ca8a04' %}{% elsif f.severity == 'LOW' %}{% assign f_border = '#6b7280' %}{% endif %}",
        '<div style="margin-bottom:2em; padding:1.25em; border:2px solid {{ f_border }}; border-radius:8px; background:#fff5f5;">',
        '  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap; margin-bottom:0.75em;">',
        '    <span style="padding:3px 10px; border-radius:12px; font-size:0.78em; font-weight:bold; background:#b91c1c; color:#fff;">🚨 Top Threat</span>',
        '    <strong style="font-size:1.15em;"><a href="/security/cves/{{ f.id }}/" style="color:#111;">{{ f.id }}</a></strong>',
        '    <span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.82em; color:#fff; background:{{ f_border }};">{{ f.severity }} {{ f.score }}</span>',
        '    {% if f.cisa_kev %}<span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.78em; color:#fff; background:#b91c1c; font-weight:bold;">⚠ EXPLOITED</span>{% endif %}',
        '    <span style="font-size:0.8em; color:#9ca3af;">{{ f.published | slice: 0, 10 }}</span>',
        '  </div>',
        '  <p style="margin:0 0 0.75em 0; color:#374151;">{{ f.description }}</p>',
        '  <div style="display:flex; gap:1.5em; flex-wrap:wrap; font-size:0.82em; color:#6b7280;">',
        '    {% if f.epss_percentile > 0 %}<span>EPSS {{ f.epss_percentile }}th percentile</span>{% endif %}',
        '    {% if f.products.size > 0 %}<span>{{ f.products | join: ", " | truncate: 80 }}</span>{% endif %}',
        '    <a href="{{ f.nvd_url }}" target="_blank" rel="noopener" style="color:#6b7280;">NVD ↗</a>',
        '  </div>',
        "</div>",
        "{% endif %}",
        "",
        "## Recent CVEs",
        "",
        "{% if site.data.cves.cves.size > 0 %}",
        "{% for cve in site.data.cves.cves %}",
        '<div style="margin-bottom:1.5em; padding:0.75em; border-left:4px solid {% if cve.severity == \'CRITICAL\' %}#dc2626{% elsif cve.severity == \'HIGH\' %}#ea580c{% elsif cve.severity == \'MEDIUM\' %}#ca8a04{% else %}#6b7280{% endif %}; background:#f9fafb;">',
        '  <strong><a href="/security/cves/{{ cve.id }}/">{{ cve.id }}</a></strong>',
        '  <a href="{{ cve.nvd_url }}" style="font-size:0.75em; color:#6b7280; margin-left:0.5em;" target="_blank" rel="noopener">NVD ↗</a>',
        '  <span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.8em; margin-left:0.5em; color:#fff; background:{% if cve.severity == \'CRITICAL\' %}#dc2626{% elsif cve.severity == \'HIGH\' %}#ea580c{% elsif cve.severity == \'MEDIUM\' %}#ca8a04{% else %}#6b7280{% endif %};">{{ cve.severity }} {{ cve.score }}</span>',
        '  {% if cve.cisa_kev %}<span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; margin-left:0.5em; color:#fff; background:#b91c1c; font-weight:bold;">⚠ EXPLOITED</span>{% endif %}',
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
        "Data from <a href=\"https://nvd.nist.gov/\">NVD</a> &middot; <a href=\"https://www.cisa.gov/known-exploited-vulnerabilities-catalog\">CISA KEV</a> &middot; <a href=\"https://www.first.org/epss/\">EPSS</a> &middot; Updated: {{ site.data.cves.generated_at }}",
        "</p>",
        "",
    ]
    return "\n".join(lines)


def _generate_cve_pages(cves):
    """Generate individual markdown pages for each CVE."""
    os.makedirs(CVE_PAGES_DIR, exist_ok=True)

    for cve in cves:
        cve_id = cve['id']
        desc_short = cve['description'].replace('"', '\\"').replace('\n', ' ').replace('\r', '')
        filepath = os.path.join(CVE_PAGES_DIR, f"{cve_id}.md")

        content = (
            "---\n"
            "layout: cve\n"
            f'cve_id: "{cve_id}"\n'
            f'title: "{cve_id} - {cve["severity"]} ({cve["score"]}) | eof.news"\n'
            f'description: "{desc_short}"\n'
            f"permalink: /security/cves/{cve_id}/\n"
            "---\n"
        )

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    print(f"✅ {len(cves)} individual CVE pages written to {CVE_PAGES_DIR}")


def publish_cves():
    """Main entry point: fetch CVEs, cross-reference, write JSON and page."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    cves = _fetch_recent_cves(days=3, max_results=50)
    print(f"Fetched {len(cves)} CVEs from NVD")

    # Cross-reference with site posts (last 30 days of security posts)
    posts = get_recent_posts(days=30, niche_filter={'security'})
    cves = _cross_reference(cves, posts)

    # Enrich with CISA KEV and EPSS data
    kev = _fetch_cisa_kev()
    cve_ids = [c['id'] for c in cves]
    epss = _fetch_epss(cve_ids)

    for cve in cves:
        cve_id = cve['id']
        # CISA KEV
        if cve_id in kev:
            cve['cisa_kev'] = True
            cve['cisa_date_added'] = kev[cve_id]['date_added']
            cve['cisa_due_date'] = kev[cve_id]['due_date']
            cve['cisa_notes'] = kev[cve_id]['notes']
            cve['cisa_required_action'] = kev[cve_id]['required_action']
        else:
            cve['cisa_kev'] = False
        # EPSS
        if cve_id in epss:
            cve['epss_score'] = epss[cve_id]['epss_score']
            cve['epss_percentile'] = epss[cve_id]['percentile']
        else:
            cve['epss_score'] = 0.0
            cve['epss_percentile'] = 0.0

    # Sort by date descending, then severity, then score
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "UNKNOWN": 4}
    cves.sort(key=lambda c: (c['published'] or '', severity_order.get(c['severity'], 5), -c['score']), reverse=True)

    featured = _pick_featured_cve(cves)

    now = datetime.now(timezone.utc)
    output = {
        "generated_at": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "total": len(cves),
        "featured_cve": featured,
        "cves": cves,
    }

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"✅ CVE JSON written: {OUTPUT_JSON}")

    page_content = _generate_page()
    with open(OUTPUT_PAGE, 'w', encoding='utf-8') as f:
        f.write(page_content)
    print(f"✅ CVE page written: {OUTPUT_PAGE}")

    _generate_cve_pages(cves)
