---
layout: page
title: "Android Dev News"
description: "Curated news for Android developers. Kotlin, Jetpack Compose, and the Android ecosystem — updated daily."
permalink: /android/
---

{% assign articles = site.data.android.articles %}

<p style="font-size:0.9em; color:#6b7280; margin-bottom:1.5em;">{{ articles.size }} articles &middot; Updated: {{ site.data.android.generated_at }}</p>

{% for article in articles %}
<div style="margin-bottom:1.25em; padding:0.85em; border:1px solid #e5e7eb; border-radius:8px;">
  <div style="margin-bottom:0.3em;">
    <strong><a href="{{ article.url }}" target="_blank" rel="noopener">{{ article.title }}</a></strong>
  </div>
  <p style="margin:0 0 0.4em 0; font-size:0.88em; color:#374151; line-height:1.5;">{{ article.excerpt }}</p>
  <span style="font-size:0.78em; color:#9ca3af;">{{ article.source }} &middot; {{ article.published | slice: 0, 10 }}</span>
</div>
{% endfor %}
