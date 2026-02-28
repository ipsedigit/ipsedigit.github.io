---
layout: page
title: "Android Dev News"
description: "Curated news for Android developers. Kotlin, Jetpack Compose, and the Android ecosystem — updated daily."
permalink: /android/
title_badge: "🤖 Android"
title_badge_bg: "#dcfce7"
title_badge_color: "#166534"
---

{% assign articles = site.data.android.articles %}
{% assign featured = articles | first %}

{% if featured %}
<div style="margin-bottom:2em; padding:1.25em; border:2px solid #16a34a; border-radius:8px; background:#f0fdf4;">
  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap; margin-bottom:0.6em;">
    <span style="padding:3px 10px; border-radius:12px; font-size:0.78em; font-weight:bold; background:#16a34a; color:#fff;">&#9733; Latest</span>
    <span style="font-size:0.78em; color:#6b7280;">{{ featured.source }} &middot; {{ featured.published | slice: 0, 10 }}</span>
  </div>
  <div style="font-weight:700; font-size:1.1em; margin-bottom:0.4em;">
    <a href="{{ featured.url }}" target="_blank" rel="noopener" style="color:#15803d; text-decoration:none;">{{ featured.title }}</a>
  </div>
  <p style="margin:0; font-size:0.88em; color:#374151; line-height:1.5;">{{ featured.excerpt }}</p>
</div>
{% endif %}

## Latest News

{% for article in articles offset:1 %}
<div style="margin-bottom:1.25em; padding:0.85em; border:1px solid #e5e7eb; border-left:3px solid #86efac; border-radius:8px;">
  <div style="margin-bottom:0.3em;">
    <strong><a href="{{ article.url }}" target="_blank" rel="noopener">{{ article.title }}</a></strong>
  </div>
  <p style="margin:0 0 0.4em 0; font-size:0.88em; color:#374151; line-height:1.5;">{{ article.excerpt }}</p>
  <span style="font-size:0.78em; color:#9ca3af;">{{ article.source }} &middot; {{ article.published | slice: 0, 10 }}</span>
</div>
{% endfor %}

---

<p style="font-size:0.8em; color:#9ca3af;">Sources: Android Developers Blog, Kotlin Blog, ProAndroidDev &middot; Updated: {{ site.data.android.generated_at }}</p>
