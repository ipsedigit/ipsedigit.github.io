---
layout: page
title: "CVE Tracker"
description: "Latest security vulnerabilities tracked daily. Critical, high, medium, and low severity CVEs with cross-references to eof.news coverage."
permalink: /security/cves/
---

## Vulnerability Summary

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
  {% if exploited > 0 %}<span style="padding:4px 12px; border-radius:12px; background:#b91c1c; color:#fff; font-weight:bold;">⚠ EXPLOITED: {{ exploited }}</span>{% endif %}
  <span style="padding:4px 12px; border-radius:12px; background:#dc2626; color:#fff; font-weight:bold;">CRITICAL: {{ critical }}</span>
  <span style="padding:4px 12px; border-radius:12px; background:#ea580c; color:#fff; font-weight:bold;">HIGH: {{ high }}</span>
  <span style="padding:4px 12px; border-radius:12px; background:#ca8a04; color:#fff; font-weight:bold;">MEDIUM: {{ medium }}</span>
  <span style="padding:4px 12px; border-radius:12px; background:#6b7280; color:#fff; font-weight:bold;">LOW: {{ low }}</span>
</div>

{% if site.data.cves.featured_cve %}
{% assign f = site.data.cves.featured_cve %}
{% assign f_border = '#dc2626' %}
{% if f.severity == 'HIGH' %}{% assign f_border = '#ea580c' %}{% elsif f.severity == 'MEDIUM' %}{% assign f_border = '#ca8a04' %}{% elsif f.severity == 'LOW' %}{% assign f_border = '#6b7280' %}{% endif %}
<div style="margin-bottom:2em; padding:1.25em; border:2px solid {{ f_border }}; border-radius:8px; background:#fff5f5;">
  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap; margin-bottom:0.75em;">
    <span style="padding:3px 10px; border-radius:12px; font-size:0.78em; font-weight:bold; background:#b91c1c; color:#fff;">🚨 Top Threat</span>
    <strong style="font-size:1.15em;"><a href="{{ f.nvd_url }}" target="_blank" rel="noopener" style="color:#111;">{{ f.id }}</a></strong>
    <span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.82em; color:#fff; background:{{ f_border }};">{{ f.severity }} {{ f.score }}</span>
    {% if f.cisa_kev %}<span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.78em; color:#fff; background:#b91c1c; font-weight:bold;">⚠ EXPLOITED</span>{% endif %}
    <span style="font-size:0.8em; color:#9ca3af;">{{ f.published | slice: 0, 10 }}</span>
  </div>
  <p style="margin:0 0 0.75em 0; color:#374151;">{{ f.description }}</p>
  <div style="display:flex; gap:1.5em; flex-wrap:wrap; font-size:0.82em; color:#6b7280;">
    {% if f.epss_percentile > 0 %}<span>EPSS {{ f.epss_percentile }}th percentile</span>{% endif %}
    {% if f.products.size > 0 %}<span>{{ f.products | join: ", " | truncate: 80 }}</span>{% endif %}
    <a href="{{ f.nvd_url }}" target="_blank" rel="noopener" style="color:#6b7280;">NVD ↗</a>
  </div>
</div>
{% endif %}

## Recent CVEs

{% if site.data.cves.cves.size > 0 %}
{% for cve in site.data.cves.cves %}
<div style="margin-bottom:1.5em; padding:0.75em; border-left:4px solid {% if cve.severity == 'CRITICAL' %}#dc2626{% elsif cve.severity == 'HIGH' %}#ea580c{% elsif cve.severity == 'MEDIUM' %}#ca8a04{% else %}#6b7280{% endif %}; background:#f9fafb;">
  <strong><a href="{{ cve.nvd_url }}" target="_blank" rel="noopener">{{ cve.id }}</a></strong>
  <span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.8em; margin-left:0.5em; color:#fff; background:{% if cve.severity == 'CRITICAL' %}#dc2626{% elsif cve.severity == 'HIGH' %}#ea580c{% elsif cve.severity == 'MEDIUM' %}#ca8a04{% else %}#6b7280{% endif %};">{{ cve.severity }} {{ cve.score }}</span>
  {% if cve.cisa_kev %}<span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; margin-left:0.5em; color:#fff; background:#b91c1c; font-weight:bold;">⚠ EXPLOITED</span>{% endif %}
  <br>
  <span style="font-size:0.9em;">{{ cve.description }}</span>
  {% if cve.products.size > 0 %}
  <br><span style="font-size:0.8em; color:#6b7280;">Products: {{ cve.products | join: ", " }}</span>
  {% endif %}
  {% if cve.related_posts.size > 0 %}
  <br><span style="font-size:0.8em;">Related: 
  {% for rp in cve.related_posts %}
    <a href="{{ rp.url }}" target="_blank" rel="noopener">{{ rp.title | truncate: 50 }}</a>{% unless forloop.last %}, {% endunless %}
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
Data from <a href="https://nvd.nist.gov/">NVD</a> &middot; <a href="https://www.cisa.gov/known-exploited-vulnerabilities-catalog">CISA KEV</a> &middot; <a href="https://www.first.org/epss/">EPSS</a> &middot; Updated: {{ site.data.cves.generated_at }}
</p>
