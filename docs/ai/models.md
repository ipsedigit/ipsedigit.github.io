---
layout: page
title: "AI Model Tracker"
description: "Trending and newly released AI models from HuggingFace, tracked daily with cross-references to eof.news coverage."
permalink: /ai/models/
---

{% include freshness-banner.html timestamp=site.data.models.generated_at %}

## Stats

<div style="display:flex; gap:1em; flex-wrap:wrap; margin-bottom:1.5em;">
  <span style="padding:4px 12px; border-radius:12px; background:#dbeafe; color:#1e40af; font-weight:bold;">Trending: {{ site.data.models.trending | size }}</span>
  <span style="padding:4px 12px; border-radius:12px; background:#dcfce7; color:#166534; font-weight:bold;">New Releases: {{ site.data.models.new_releases | size }}</span>
</div>

{% assign cats = '' %}
{% for m in site.data.models.trending %}
  {% unless cats contains m.category %}
    {% if cats != '' %}{% assign cats = cats | append: ',' %}{% endif %}
    {% assign cats = cats | append: m.category %}
  {% endunless %}
{% endfor %}

## Trending Models

{% if site.data.models.trending.size > 0 %}
{% for model in site.data.models.trending %}
<div style="margin-bottom:1.2em; padding:0.75em; border:1px solid #e5e7eb; border-radius:8px;">
  <strong><a href="{{ model.url }}">{{ model.model_id }}</a></strong>
  {% if model.category %}
    <span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; margin-left:0.5em; background:{% if model.category == 'Language Model' %}#8b5cf6{% elsif model.category == 'Image Generation' %}#ec4899{% elsif model.category == 'Computer Vision' %}#06b6d4{% elsif model.category == 'Speech' or model.category == 'Audio' %}#f59e0b{% elsif model.category == 'Embeddings' %}#10b981{% else %}#6366f1{% endif %};">{{ model.category }}</span>
  {% endif %}
  <br>
  <span style="font-size:0.85em; color:#6b7280;">
    by {{ model.author }}
    &middot; &#10515; {{ model.downloads }}
    &middot; &#9829; {{ model.likes }}
  </span>
  {% if model.related_posts.size > 0 %}
  <br><span style="font-size:0.8em;">Coverage: 
  {% for rp in model.related_posts %}
    <a href="{{ rp.url }}">{{ rp.title | truncate: 50 }}</a>{% unless forloop.last %}, {% endunless %}
  {% endfor %}
  </span>
  {% endif %}
</div>
{% endfor %}
{% else %}
<p>No trending models data yet. Check back after the next update.</p>
{% endif %}

## New Releases (Last 7 Days)

{% if site.data.models.new_releases.size > 0 %}
{% for model in site.data.models.new_releases %}
<div style="margin-bottom:1em; padding:0.5em 0; border-bottom:1px solid #e5e7eb;">
  <strong><a href="{{ model.url }}">{{ model.model_id }}</a></strong>
  {% if model.category %}
    <span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; background:{% if model.category == 'Language Model' %}#8b5cf6{% elsif model.category == 'Image Generation' %}#ec4899{% elsif model.category == 'Computer Vision' %}#06b6d4{% elsif model.category == 'Speech' or model.category == 'Audio' %}#f59e0b{% elsif model.category == 'Embeddings' %}#10b981{% else %}#6366f1{% endif %};">{{ model.category }}</span>
  {% endif %}
  <br>
  <span style="font-size:0.85em; color:#6b7280;">
    by {{ model.author }}
    &middot; &#10515; {{ model.downloads }}
    &middot; Created: {{ model.created_at }}
  </span>
</div>
{% endfor %}
{% else %}
<p>No new releases this week.</p>
{% endif %}

---

<p style="font-size:0.8em; color:#9ca3af;">
Data from <a href="https://huggingface.co/">HuggingFace</a>
</p>
