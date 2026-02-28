---
layout: page
title: "Service Outages"
description: "Real-time outage tracker for major developer services. GitHub, AWS, GCP, Cloudflare, Stripe, and more."
permalink: /outages/
title_badge: "⚠ Outages"
title_badge_bg: "#fef2f2"
title_badge_color: "#b91c1c"
---

{% assign active = site.data.outages.active %}
{% assign resolved = site.data.outages.resolved_24h %}
{% assign featured = active | first %}

{% if featured %}
<div style="margin-bottom:2em; padding:1.25em; border:2px solid #dc2626; border-radius:8px; background:#fef2f2;">
  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap; margin-bottom:0.6em;">
    <span style="padding:3px 10px; border-radius:12px; font-size:0.78em; font-weight:bold; background:#dc2626; color:#fff;">⚠ Active Incident</span>
    <span style="font-size:0.78em; color:#6b7280;">{{ featured.service }} &middot; Started {{ featured.started_at | slice: 0, 16 | replace: 'T', ' ' }} UTC</span>
  </div>
  <div style="font-weight:700; font-size:1.1em; margin-bottom:0.4em;">
    <a href="{{ featured.shortlink }}" target="_blank" rel="noopener" style="color:#b91c1c; text-decoration:none;">{{ featured.name }}</a>
    <span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; text-decoration:none; margin-left:0.4em; background:{% if featured.impact == 'critical' %}#7f1d1d{% elsif featured.impact == 'major' %}#dc2626{% elsif featured.impact == 'minor' %}#ca8a04{% else %}#6b7280{% endif %};">{{ featured.impact | upcase }}</span>
  </div>
  <p style="margin:0; font-size:0.88em; color:#374151; line-height:1.5;">{{ featured.status | capitalize }} &middot; Updated {{ featured.updated_at | slice: 0, 16 | replace: 'T', ' ' }} UTC</p>
</div>
{% endif %}

{% if active.size > 0 %}
<h3 style="margin-top:0; margin-bottom:0.75em; font-size:1em; color:#b91c1c;">Active Incidents ({{ site.data.outages.active_count }})</h3>
{% for incident in active %}
<div style="margin-bottom:1.25em; padding:0.85em; border:1px solid #fca5a5; border-left:3px solid {% if incident.impact == 'critical' %}#7f1d1d{% elsif incident.impact == 'major' %}#dc2626{% elsif incident.impact == 'minor' %}#ca8a04{% else %}#6b7280{% endif %}; border-radius:8px;">
  <div style="margin-bottom:0.3em;">
    <strong><a href="{{ incident.shortlink }}" target="_blank" rel="noopener">{{ incident.name }}</a></strong>
    <span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; margin-left:0.4em; background:{% if incident.impact == 'critical' %}#7f1d1d{% elsif incident.impact == 'major' %}#dc2626{% elsif incident.impact == 'minor' %}#ca8a04{% else %}#6b7280{% endif %};">{{ incident.impact | upcase }}</span>
  </div>
  <span style="font-size:0.78em; color:#9ca3af;">{{ incident.service }} &middot; {{ incident.status | capitalize }} &middot; Started {{ incident.started_at | slice: 0, 16 | replace: 'T', ' ' }} UTC</span>
</div>
{% endfor %}
{% else %}
<p style="color:#16a34a; font-weight:bold;">✅ All systems operational</p>
{% endif %}

{% if resolved.size > 0 %}
<h3 style="margin-top:2em; margin-bottom:0.75em; font-size:1em; color:#6b7280;">Resolved (last 24h)</h3>
{% for incident in resolved %}
<div style="margin-bottom:1.25em; padding:0.85em; border:1px solid #e5e7eb; border-left:3px solid #d1d5db; border-radius:8px; opacity:0.85;">
  <div style="margin-bottom:0.3em;">
    <strong><a href="{{ incident.shortlink }}" target="_blank" rel="noopener" style="color:#374151;">{{ incident.name }}</a></strong>
  </div>
  <span style="font-size:0.78em; color:#9ca3af;">{{ incident.service }} &middot; ✅ Resolved {{ incident.resolved_at | slice: 0, 16 | replace: 'T', ' ' }} UTC</span>
</div>
{% endfor %}
{% endif %}

---

<p style="font-size:0.8em; color:#9ca3af;">Data from statuspage.io APIs &middot; Updated: {{ site.data.outages.generated_at }}</p>
