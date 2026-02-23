---
layout: page
title: "CVE Tracker"
description: "Latest security vulnerabilities tracked daily. Critical, high, medium, and low severity CVEs with cross-references to eof.news coverage."
permalink: /security/cves/
---

## Vulnerability Summary

{% assign critical = 0 %}{% assign high = 0 %}{% assign medium = 0 %}{% assign low = 0 %}
{% for cve in site.data.cves.cves %}
  {% if cve.severity == "CRITICAL" %}{% assign critical = critical | plus: 1 %}
  {% elsif cve.severity == "HIGH" %}{% assign high = high | plus: 1 %}
  {% elsif cve.severity == "MEDIUM" %}{% assign medium = medium | plus: 1 %}
  {% elsif cve.severity == "LOW" %}{% assign low = low | plus: 1 %}
  {% endif %}
{% endfor %}

<div style="display:flex; gap:1em; flex-wrap:wrap; margin-bottom:1.5em;">
  <span style="padding:4px 12px; border-radius:12px; background:#dc2626; color:#fff; font-weight:bold;">CRITICAL: {{ critical }}</span>
  <span style="padding:4px 12px; border-radius:12px; background:#ea580c; color:#fff; font-weight:bold;">HIGH: {{ high }}</span>
  <span style="padding:4px 12px; border-radius:12px; background:#ca8a04; color:#fff; font-weight:bold;">MEDIUM: {{ medium }}</span>
  <span style="padding:4px 12px; border-radius:12px; background:#6b7280; color:#fff; font-weight:bold;">LOW: {{ low }}</span>
</div>

## Recent CVEs

{% if site.data.cves.cves.size > 0 %}
{% for cve in site.data.cves.cves %}
<div style="margin-bottom:1.5em; padding:0.75em; border-left:4px solid {% if cve.severity == 'CRITICAL' %}#dc2626{% elsif cve.severity == 'HIGH' %}#ea580c{% elsif cve.severity == 'MEDIUM' %}#ca8a04{% else %}#6b7280{% endif %}; background:#f9fafb;">
  <strong><a href="{{ cve.nvd_url }}">{{ cve.id }}</a></strong>
  <span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.8em; margin-left:0.5em; color:#fff; background:{% if cve.severity == 'CRITICAL' %}#dc2626{% elsif cve.severity == 'HIGH' %}#ea580c{% elsif cve.severity == 'MEDIUM' %}#ca8a04{% else %}#6b7280{% endif %};">{{ cve.severity }} {{ cve.score }}</span>
  <br>
  <span style="font-size:0.9em;">{{ cve.description }}</span>
  {% if cve.products.size > 0 %}
  <br><span style="font-size:0.8em; color:#6b7280;">Products: {{ cve.products | join: ", " }}</span>
  {% endif %}
  {% if cve.related_posts.size > 0 %}
  <br><span style="font-size:0.8em;">Related: 
  {% for rp in cve.related_posts %}
    <a href="{{ rp.url }}">{{ rp.title | truncate: 50 }}</a>{% unless forloop.last %}, {% endunless %}
  {% endfor %}
  </span>
  {% endif %}
</div>
{% endfor %}
{% else %}
<p>No CVEs tracked yet. Check back after the next update.</p>
{% endif %}

---

<p style="font-size:0.8em; color:#9ca3af;">
Data from <a href="https://nvd.nist.gov/">NVD</a> &middot; Updated: {{ site.data.cves.generated_at }}
</p>
