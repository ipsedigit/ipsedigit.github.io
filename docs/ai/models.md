---
layout: page
title: "AI Model Tracker"
description: "Trending and newly released AI models from HuggingFace, tracked daily with cross-references to eof.news coverage."
permalink: /ai/models/
---

## Stats

<div style="display:flex; gap:1em; flex-wrap:wrap; margin-bottom:1.5em;">
  <a href="#trending-models" style="padding:4px 12px; border-radius:12px; background:#dbeafe; color:#1e40af; font-weight:bold; text-decoration:none; cursor:pointer;">Trending: {{ site.data.models.trending | size }}</a>
  <a href="#new-releases" style="padding:4px 12px; border-radius:12px; background:#dcfce7; color:#166534; font-weight:bold; text-decoration:none; cursor:pointer;">New Releases: {{ site.data.models.new_releases | size }}</a>
</div>

{% if site.data.models.featured_model %}
{% assign f = site.data.models.featured_model %}
<div style="margin-bottom:2em; padding:1.25em; border:2px solid #8b5cf6; border-radius:8px; background:#faf5ff;">
  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap; margin-bottom:0.75em;">
    <a href="{{ f.url }}" target="_blank" rel="noopener" style="padding:3px 10px; border-radius:12px; font-size:0.78em; font-weight:bold; background:#8b5cf6; color:#fff; text-decoration:none;">✦ Model of the Day</a>
    <strong style="font-size:1.15em;"><a href="{{ f.url }}" target="_blank" rel="noopener" style="color:#111;">{{ f.model_id }}</a></strong>
    {% if f.category %}<a href="/niche/ai/" style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.78em; color:#fff; text-decoration:none; background:#8b5cf6;">{{ f.category }}</a>{% endif %}
    {% if f.like_delta > 0 %}<span style="font-size:0.82em; color:#059669; font-weight:bold;">🔥 +{{ f.like_delta }} likes</span>{% endif %}
  </div>
  <div style="display:flex; gap:1.5em; flex-wrap:wrap; font-size:0.82em; color:#6b7280;">
    <span>by {{ f.author }}</span>
    <span>&#10515; {{ f.downloads }}</span>
    <span>&#9829; {{ f.likes }}</span>
    {% if f.created_at %}<span>Released {{ f.created_at }}</span>{% endif %}
  </div>
  {% if f.tags.size > 0 %}
  <div style="margin-top:0.6em; display:flex; gap:0.4em; flex-wrap:wrap;">
    {% for tag in f.tags limit:4 %}
    {% assign tag_slug = tag | slugify %}<a href="/tags/{{ tag_slug }}/" style="padding:2px 6px; background:#ede9fe; color:#6d28d9; border-radius:4px; font-size:0.75em; text-decoration:none;">{{ tag }}</a>
    {% endfor %}
  </div>
  {% endif %}
</div>
{% endif %}

## Trending Models {#trending-models}

{% if site.data.models.trending.size > 0 %}
{% for model in site.data.models.trending %}
<div style="margin-bottom:1.2em; padding:0.75em; border:1px solid #e5e7eb; border-radius:8px;">
  <strong><a href="{{ model.url }}" target="_blank" rel="noopener">{{ model.model_id }}</a></strong>
  {% if model.category %}
    {% assign cat_slug = model.category | slugify %}<a href="/ai/models/#{{ cat_slug }}" style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; text-decoration:none; margin-left:0.5em; background:{% if model.category == 'Language Model' %}#8b5cf6{% elsif model.category == 'Image Generation' %}#ec4899{% elsif model.category == 'Computer Vision' %}#06b6d4{% elsif model.category == 'Speech' or model.category == 'Audio' %}#f59e0b{% elsif model.category == 'Embeddings' %}#10b981{% else %}#6366f1{% endif %};">{{ model.category }}</a>
  {% endif %}
  {% if model.like_delta > 0 %}<span style="font-size:0.78em; color:#059669; margin-left:0.5em;">▲ +{{ model.like_delta }}</span>{% endif %}
  <br>
  <span style="font-size:0.85em; color:#6b7280;">
    by {{ model.author }}
    &middot; &#10515; {{ model.downloads }}
    &middot; &#9829; {{ model.likes }}
  </span>
  {% if model.related_posts.size > 0 %}
  <br><span style="font-size:0.8em;">Coverage: 
  {% for rp in model.related_posts %}
    <a href="{{ rp.url }}" target="_blank" rel="noopener">{{ rp.title | truncate: 50 }}</a>{% unless forloop.last %}, {% endunless %}
  {% endfor %}
  </span>
  {% endif %}
</div>
{% endfor %}
{% else %}
<p>No trending models data yet. Check back after the next update.</p>
{% endif %}

## New Releases (Last 7 Days) {#new-releases}

{% if site.data.models.new_releases.size > 0 %}
{% for model in site.data.models.new_releases %}
<div style="margin-bottom:1em; padding:0.75em; border:1px solid #e5e7eb; border-radius:8px;">
  <strong><a href="{{ model.url }}" target="_blank" rel="noopener">{{ model.model_id }}</a></strong>
  {% if model.category %}
    {% assign cat_slug = model.category | slugify %}<a href="/ai/models/#{{ cat_slug }}" style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; text-decoration:none; background:{% if model.category == 'Language Model' %}#8b5cf6{% elsif model.category == 'Image Generation' %}#ec4899{% elsif model.category == 'Computer Vision' %}#06b6d4{% elsif model.category == 'Speech' or model.category == 'Audio' %}#f59e0b{% elsif model.category == 'Embeddings' %}#10b981{% else %}#6366f1{% endif %};">{{ model.category }}</a>
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
Data from <a href="https://huggingface.co/">HuggingFace</a> &middot; Updated: {{ site.data.models.generated_at }}
</p>
