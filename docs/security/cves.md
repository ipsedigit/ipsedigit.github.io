---
layout: page
title: "CVE Tracker"
description: "Latest security vulnerabilities tracked daily. Critical, high, medium, and low severity CVEs with cross-references to eof.news coverage."
permalink: /security/cves/
title_badge: "🔒 CVEs"
title_badge_bg: "#fef2f2"
title_badge_color: "#b91c1c"
---

{% assign critical = 0 %}{% assign high = 0 %}{% assign medium = 0 %}{% assign low = 0 %}{% assign exploited = 0 %}
{% for cve in site.data.cves.cves %}
  {% if cve.severity == "CRITICAL" %}{% assign critical = critical | plus: 1 %}
  {% elsif cve.severity == "HIGH" %}{% assign high = high | plus: 1 %}
  {% elsif cve.severity == "MEDIUM" %}{% assign medium = medium | plus: 1 %}
  {% elsif cve.severity == "LOW" %}{% assign low = low | plus: 1 %}
  {% endif %}
  {% if cve.cisa_kev %}{% assign exploited = exploited | plus: 1 %}{% endif %}
{% endfor %}

<div style="display:flex; gap:1em; flex-wrap:wrap; margin-bottom:1.5em;">
  {% if exploited > 0 %}<a href="#cve-exploited" style="padding:4px 12px; border-radius:12px; background:#b91c1c; color:#fff; font-weight:bold; text-decoration:none;">⚠ EXPLOITED: {{ exploited }}</a>{% endif %}
  <a href="#cve-critical" style="padding:4px 12px; border-radius:12px; background:#dc2626; color:#fff; font-weight:bold; text-decoration:none;">CRITICAL: {{ critical }}</a>
  <a href="#cve-high" style="padding:4px 12px; border-radius:12px; background:#ea580c; color:#fff; font-weight:bold; text-decoration:none;">HIGH: {{ high }}</a>
  <a href="#cve-medium" style="padding:4px 12px; border-radius:12px; background:#ca8a04; color:#fff; font-weight:bold; text-decoration:none;">MEDIUM: {{ medium }}</a>
  <a href="#cve-low" style="padding:4px 12px; border-radius:12px; background:#6b7280; color:#fff; font-weight:bold; text-decoration:none;">LOW: {{ low }}</a>
</div>

{% if site.data.cves.featured_cve %}
{% assign f = site.data.cves.featured_cve %}
{% assign f_border = '#dc2626' %}{% assign f_bg = '#fef2f2' %}
{% if f.severity == 'HIGH' %}{% assign f_border = '#ea580c' %}{% assign f_bg = '#fff7ed' %}{% elsif f.severity == 'MEDIUM' %}{% assign f_border = '#ca8a04' %}{% assign f_bg = '#fefce8' %}{% elsif f.severity == 'LOW' %}{% assign f_border = '#6b7280' %}{% assign f_bg = '#f9fafb' %}{% endif %}
<div style="margin-bottom:2em; padding:1.25em; border:2px solid {{ f_border }}; border-radius:8px; background:{{ f_bg }};">
  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap; margin-bottom:0.6em;">
    <span style="padding:3px 10px; border-radius:12px; font-size:0.78em; font-weight:bold; background:#b91c1c; color:#fff;">🚨 Top Threat</span>
    <span style="font-size:0.78em; color:#6b7280;">{{ f.id }} &middot; {{ f.published | slice: 0, 10 }}</span>
  </div>
  <div style="font-weight:700; font-size:1.1em; margin-bottom:0.4em;">
    <a href="{{ f.nvd_url }}" target="_blank" rel="noopener" style="color:#111; text-decoration:none;">{{ f.id }}</a>
    <a href="#cve-{{ f.severity | downcase }}" style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; text-decoration:none; margin-left:0.4em; background:{{ f_border }};">{{ f.severity }} {{ f.score }}</a>
    {% if f.cisa_kev %}<span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; background:#b91c1c; font-weight:bold; margin-left:0.4em;">⚠ EXPLOITED</span>{% endif %}
  </div>
  <p style="margin:0 0 0.4em 0; font-size:0.88em; color:#374151; line-height:1.5;">{{ f.description }}</p>
  <span style="font-size:0.78em; color:#9ca3af;">
    {% if f.epss_percentile > 0 %}EPSS {{ f.epss_percentile }}th percentile &middot; {% endif %}
    {% if f.products.size > 0 %}{{ f.products | join: ", " | truncate: 80 }} &middot; {% endif %}
    <a href="{{ f.nvd_url }}" target="_blank" rel="noopener" style="color:#9ca3af;">NVD ↗</a>
  </span>
</div>
{% endif %}

{% if site.data.cves.cves.size > 0 %}
{% assign seen_critical = false %}{% assign seen_high = false %}{% assign seen_medium = false %}{% assign seen_low = false %}{% assign seen_exploited = false %}
{% for cve in site.data.cves.cves %}
{% assign sev_lower = cve.severity | downcase %}
{% assign sev_color = '#6b7280' %}
{% if cve.severity == 'CRITICAL' %}{% assign sev_color = '#dc2626' %}{% elsif cve.severity == 'HIGH' %}{% assign sev_color = '#ea580c' %}{% elsif cve.severity == 'MEDIUM' %}{% assign sev_color = '#ca8a04' %}{% endif %}
<div id="{% if cve.cisa_kev and seen_exploited == false %}cve-exploited{% endif %}" style="margin-bottom:1.25em; padding:0.85em; border:1px solid #e5e7eb; border-left:3px solid {{ sev_color }}; border-radius:8px;">
{% if sev_lower == 'critical' and seen_critical == false %}<span id="cve-critical"></span>{% assign seen_critical = true %}{% endif %}
{% if sev_lower == 'high' and seen_high == false %}<span id="cve-high"></span>{% assign seen_high = true %}{% endif %}
{% if sev_lower == 'medium' and seen_medium == false %}<span id="cve-medium"></span>{% assign seen_medium = true %}{% endif %}
{% if sev_lower == 'low' and seen_low == false %}<span id="cve-low"></span>{% assign seen_low = true %}{% endif %}
{% if cve.cisa_kev and seen_exploited == false %}{% assign seen_exploited = true %}{% endif %}
  <div style="margin-bottom:0.3em;">
    <strong><a href="{{ cve.nvd_url }}" target="_blank" rel="noopener">{{ cve.id }}</a></strong>
    <a href="#cve-{{ sev_lower }}" style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; text-decoration:none; margin-left:0.4em; background:{{ sev_color }};">{{ cve.severity }} {{ cve.score }}</a>
    {% if cve.cisa_kev %}<span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; background:#b91c1c; font-weight:bold; margin-left:0.4em;">⚠ EXPLOITED</span>{% endif %}
  </div>
  <p style="margin:0 0 0.4em 0; font-size:0.88em; color:#374151; line-height:1.5;">{{ cve.description }}</p>
  <span style="font-size:0.78em; color:#9ca3af;">
    {% if cve.products.size > 0 %}{{ cve.products | join: ", " }}{% endif %}
    {% if cve.related_posts.size > 0 %} &middot; Coverage:
      {% for rp in cve.related_posts %}<a href="{{ rp.url }}" target="_blank" rel="noopener" style="color:#9ca3af;">{{ rp.title | truncate: 50 }}</a>{% unless forloop.last %}, {% endunless %}{% endfor %}
    {% endif %}
  </span>
</div>
{% endfor %}
{% else %}
<p>No CVEs tracked yet. Check back after the next update.</p>
{% endif %}

---

<p style="font-size:0.8em; color:#9ca3af;">
Data from <a href="https://nvd.nist.gov/">NVD</a> &middot; <a href="https://www.cisa.gov/known-exploited-vulnerabilities-catalog">CISA KEV</a> &middot; <a href="https://www.first.org/epss/">EPSS</a> &middot; Updated: {{ site.data.cves.generated_at }}
</p>
