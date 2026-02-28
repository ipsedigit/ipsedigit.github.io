---
layout: page
title: "iOS Dev News"
description: "Curated news for iOS developers. Swift, SwiftUI, Xcode, and the Apple dev ecosystem — updated daily."
permalink: /ios/
---

{% assign articles = site.data.ios.articles %}
{% assign featured = articles | first %}

<div style="display:flex; gap:1em; flex-wrap:wrap; margin-bottom:1.5em;">
  <span style="padding:4px 12px; border-radius:12px; background:#dbeafe; color:#1e40af; font-weight:bold;">🍎 iOS</span>
  <span style="padding:4px 12px; border-radius:12px; background:#f3f4f6; color:#374151; font-weight:bold;">{{ articles.size }} articles</span>
  <span style="padding:4px 12px; border-radius:12px; background:#f3f4f6; color:#374151; font-weight:bold;">3 sources</span>
  <span style="padding:4px 12px; border-radius:12px; background:#f3f4f6; color:#6b7280; font-size:0.85em;">Updated: {{ site.data.ios.generated_at }}</span>
</div>

{% if featured %}
<div style="margin-bottom:2em; padding:1.25em; border:2px solid #0071e3; border-radius:8px; background:#f0f7ff;">
  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap; margin-bottom:0.6em;">
    <span style="padding:3px 10px; border-radius:12px; font-size:0.78em; font-weight:bold; background:#0071e3; color:#fff;">&#9733; Latest</span>
    <span style="font-size:0.78em; color:#6b7280;">{{ featured.source }} &middot; {{ featured.published | slice: 0, 10 }}</span>
  </div>
  <div style="font-weight:700; font-size:1.1em; margin-bottom:0.4em;">
    <a href="{{ featured.url }}" target="_blank" rel="noopener" style="color:#0071e3; text-decoration:none;">{{ featured.title }}</a>
  </div>
  <p style="margin:0; font-size:0.88em; color:#374151; line-height:1.5;">{{ featured.excerpt }}</p>
</div>
{% endif %}

{% for article in articles offset:1 %}
<div style="margin-bottom:1.25em; padding:0.85em; border:1px solid #e5e7eb; border-left:3px solid #93c5fd; border-radius:8px;">
  <div style="margin-bottom:0.3em;">
    <strong><a href="{{ article.url }}" target="_blank" rel="noopener">{{ article.title }}</a></strong>
  </div>
  <p style="margin:0 0 0.4em 0; font-size:0.88em; color:#374151; line-height:1.5;">{{ article.excerpt }}</p>
  <span style="font-size:0.78em; color:#9ca3af;">{{ article.source }} &middot; {{ article.published | slice: 0, 10 }}</span>
</div>
{% endfor %}
