---
layout: page
title: "AI Model Tracker"
description: "Trending and newly released AI models from HuggingFace, tracked daily with cross-references to eof.news coverage."
permalink: /ai/models/
title_badge: "✦ AI Models"
title_badge_bg: "#ede9fe"
title_badge_color: "#6d28d9"
---

<div style="display:flex; gap:1em; flex-wrap:wrap; margin-bottom:1.5em;">
  <span style="padding:4px 12px; border-radius:12px; background:#ede9fe; color:#6d28d9; font-weight:bold;">✦ AI Models</span>
  <span style="padding:4px 12px; border-radius:12px; background:#f3f4f6; color:#374151; font-weight:bold;">{{ site.data.models.trending | size }} trending</span>
  {% if site.data.models.new_releases.size > 0 %}<span style="padding:4px 12px; border-radius:12px; background:#f3f4f6; color:#374151; font-weight:bold;">{{ site.data.models.new_releases | size }} new</span>{% endif %}
</div>

{% if site.data.models.featured_model %}
{% assign f = site.data.models.featured_model %}
<div style="margin-bottom:2em; padding:1.25em; border:2px solid #8b5cf6; border-radius:8px; background:#faf5ff;">
  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap; margin-bottom:0.6em;">
    <span style="padding:3px 10px; border-radius:12px; font-size:0.78em; font-weight:bold; background:#8b5cf6; color:#fff;">✦ Model of the Day</span>
    <span style="font-size:0.78em; color:#6b7280;">{{ f.author }}{% if f.created_at %} &middot; {{ f.created_at }}{% endif %}</span>
  </div>
  <div style="font-weight:700; font-size:1.1em; margin-bottom:0.4em;">
    <a href="{{ f.url }}" target="_blank" rel="noopener" style="color:#6d28d9; text-decoration:none;">{{ f.model_id }}</a>
    {% if f.category %}<a href="/niche/ai/" style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; text-decoration:none; background:#8b5cf6; margin-left:0.4em;">{{ f.category }}</a>{% endif %}
    {% if f.like_delta > 0 %}<span style="font-size:0.82em; color:#059669; font-weight:bold; margin-left:0.4em;">🔥 +{{ f.like_delta }} likes</span>{% endif %}
  </div>
  <p style="margin:0 0 0.4em 0; font-size:0.88em; color:#374151; line-height:1.5;">&#10515; {{ f.downloads }} &nbsp;&#9829; {{ f.likes }}</p>
  {% if f.tags.size > 0 %}
  <div style="display:flex; gap:0.4em; flex-wrap:wrap;">
    {% for tag in f.tags limit:4 %}
    {% assign tag_slug = tag | slugify %}<a href="/tags/{{ tag_slug }}/" style="padding:2px 6px; background:#ede9fe; color:#6d28d9; border-radius:4px; font-size:0.75em; text-decoration:none;">{{ tag }}</a>
    {% endfor %}
  </div>
  {% endif %}
</div>
{% endif %}

{% if site.data.models.trending.size > 0 %}
{% for model in site.data.models.trending %}
<div style="margin-bottom:1.25em; padding:0.85em; border:1px solid #e5e7eb; border-left:3px solid #c4b5fd; border-radius:8px;">
  <div style="margin-bottom:0.3em;">
    <strong><a href="{{ model.url }}" target="_blank" rel="noopener">{{ model.model_id }}</a></strong>
    {% if model.category %}
      {% assign cat_slug = model.category | slugify %}<a href="/ai/models/#{{ cat_slug }}" style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; text-decoration:none; margin-left:0.4em; background:{% if model.category == 'Language Model' %}#8b5cf6{% elsif model.category == 'Image Generation' %}#ec4899{% elsif model.category == 'Computer Vision' %}#06b6d4{% elsif model.category == 'Speech' or model.category == 'Audio' %}#f59e0b{% elsif model.category == 'Embeddings' %}#10b981{% else %}#6366f1{% endif %};">{{ model.category }}</a>
    {% endif %}
    {% if model.like_delta > 0 %}<span style="font-size:0.78em; color:#059669; margin-left:0.4em;">▲ +{{ model.like_delta }}</span>{% endif %}
  </div>
  <span style="font-size:0.78em; color:#9ca3af;">by {{ model.author }} &middot; &#10515; {{ model.downloads }} &middot; &#9829; {{ model.likes }}</span>
  {% if model.related_posts.size > 0 %}
  <div style="margin-top:0.3em; font-size:0.8em;">Coverage:
    {% for rp in model.related_posts %}
      <a href="{{ rp.url }}" target="_blank" rel="noopener">{{ rp.title | truncate: 50 }}</a>{% unless forloop.last %}, {% endunless %}
    {% endfor %}
  </div>
  {% endif %}
</div>
{% endfor %}
{% else %}
<p>No trending models data yet. Check back after the next update.</p>
{% endif %}

{% if site.data.models.new_releases.size > 0 %}
<h3 style="margin-top:2em; margin-bottom:0.75em; font-size:1em; color:#6d28d9;">New Releases</h3>
{% for model in site.data.models.new_releases %}
<div style="margin-bottom:1.25em; padding:0.85em; border:1px solid #e5e7eb; border-left:3px solid #c4b5fd; border-radius:8px;">
  <div style="margin-bottom:0.3em;">
    <strong><a href="{{ model.url }}" target="_blank" rel="noopener">{{ model.model_id }}</a></strong>
    {% if model.category %}
      {% assign cat_slug = model.category | slugify %}<a href="/ai/models/#{{ cat_slug }}" style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; text-decoration:none; margin-left:0.4em; background:{% if model.category == 'Language Model' %}#8b5cf6{% elsif model.category == 'Image Generation' %}#ec4899{% elsif model.category == 'Computer Vision' %}#06b6d4{% elsif model.category == 'Speech' or model.category == 'Audio' %}#f59e0b{% elsif model.category == 'Embeddings' %}#10b981{% else %}#6366f1{% endif %};">{{ model.category }}</a>
    {% endif %}
  </div>
  <span style="font-size:0.78em; color:#9ca3af;">by {{ model.author }} &middot; &#10515; {{ model.downloads }} &middot; Created: {{ model.created_at }}</span>
</div>
{% endfor %}
{% endif %}

---

<p style="font-size:0.8em; color:#9ca3af;">
Data from <a href="https://huggingface.co/">HuggingFace</a> &middot; Updated: {{ site.data.models.generated_at }}
</p>
