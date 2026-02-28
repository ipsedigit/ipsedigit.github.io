---
layout: page
title: "Devs"
description: "Personal blogs by individual developers. Raw, unfiltered, not mainstream."
permalink: /devs/
title_badge: "✍️ Devs"
title_badge_bg: "#eef2ff"
title_badge_color: "#4f46e5"
---

<style>
/* Post cards */
.post-item {
  padding: 1.25rem;
  margin-bottom: 1rem;
  border: 1px solid #e5e5e5;
  border-radius: 6px;
  background: #fafafa;
}
.post-item:hover {
  border-color: #ccc;
}
.post-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  line-height: 1.4;
}
.post-title a { color: #111; text-decoration: none; }
.post-title a:hover { color: #4f46e5; }
.post-meta {
  font-size: 0.8rem;
  color: #888;
  margin-bottom: 0.5rem;
}
.post-preview {
  color: #444;
  font-size: 0.9rem;
  margin: 0.5rem 0 0 0;
  line-height: 1.5;
}

/* Source badge */
.source-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 3px;
  font-size: 0.7rem;
  font-weight: 600;
  color: #fff;
  text-decoration: none;
  cursor: pointer;
}
.source-badge:hover { opacity: 0.85; }
.source-badge--julia-evans            { background: #059669; }
.source-badge--dan-luu                { background: #d97706; }
.source-badge--computer-enhance       { background: #dc2626; }
.source-badge--sean-goedecke          { background: #7c3aed; }
.source-badge--marc-brooker           { background: #0284c7; }
.source-badge--rachel-by-the-bay      { background: #db2777; }
.source-badge--chris-wellons          { background: #374151; }
.source-badge--armin-ronacher         { background: #b45309; }
.source-badge--mitchell-hashimoto     { background: #0891b2; }
.source-badge--drew-devault           { background: #4f46e5; }
.source-badge--antirez                { background: #c2410c; }
.source-badge--matthew-green          { background: #6366f1; }
.source-badge--jessie-frazelle        { background: #0f766e; }
.source-badge--ken-shirriff           { background: #92400e; }

/* Links-back section */
.devs-links-back {
  margin-top: 2.5rem;
}
.devs-links-back h2 {
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #eee;
}
.devs-links-back p.sub {
  color: #666;
  font-size: 0.85rem;
  margin-bottom: 1rem;
}
.devs-links-back .source-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 0.75rem;
}
.devs-links-back .source-item {
  background: #fafafa;
  border: 1px solid #e5e5e5;
  border-radius: 6px;
  padding: 1rem;
}
.devs-links-back .source-item a {
  color: #111;
  text-decoration: none;
  font-weight: 500;
}
.devs-links-back .source-item a:hover {
  color: #4f46e5;
}
</style>

{% if site.data.devs_articles and site.data.devs_articles.articles and site.data.devs_articles.articles.size > 0 %}

{% assign featured = site.data.devs_articles.articles | first %}
{% assign hero_slug = featured.source | slugify %}

<div style="margin-bottom:2em; padding:1.25em; border:2px solid #4f46e5; border-radius:8px; background:#eef2ff;">
  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap; margin-bottom:0.6em;">
    <span style="padding:3px 10px; border-radius:12px; font-size:0.78em; font-weight:bold; background:#4f46e5; color:#fff;">&#9733; Latest</span>
    <span style="font-size:0.78em; color:#6b7280;"><a href="/devs/#{{ hero_slug }}" class="source-badge source-badge--{{ hero_slug }}">{{ featured.source }}</a> &middot; {{ featured.date }}</span>
  </div>
  <div style="font-weight:700; font-size:1.1em; margin-bottom:0.4em;">
    <a href="{{ featured.url }}" target="_blank" rel="noopener" style="color:#4f46e5; text-decoration:none;">{{ featured.title | escape }}</a>
  </div>
  {% if featured.description and featured.description != "" %}
  <p style="margin:0; font-size:0.88em; color:#374151; line-height:1.5;">{{ featured.description | truncate: 200 }}</p>
  {% endif %}
</div>

{% assign anchored_sources = "" %}
{% for art in site.data.devs_articles.articles offset:1 %}
{% assign src_slug = art.source | slugify %}
{% unless anchored_sources contains src_slug %}
{% assign anchored_sources = anchored_sources | append: src_slug | append: "|" %}
<article class="post-item" id="{{ src_slug }}">
{% else %}
<article class="post-item">
{% endunless %}
  <h2 class="post-title">
    <a href="{{ art.url }}" target="_blank" rel="noopener">{{ art.title | escape }}</a>
  </h2>
  <div class="post-meta">
    {{ art.date }}
    · <a href="/devs/#{{ src_slug }}" class="source-badge source-badge--{{ src_slug }}">{{ art.source }}</a>
  </div>
  {% if art.description and art.description != "" %}
  <p class="post-preview">{{ art.description | truncate: 160 }}</p>
  {% endif %}
</article>
{% endfor %}

{% else %}
<p>No articles yet.</p>
{% endif %}

<div class="devs-links-back">
<h2>Who links to us</h2>
<p class="sub">Sites that link back to eof.news. If you link to us, <a href="/about/">tell us</a> and we'll add you here.</p>
<div class="source-list">
{% if site.data.links_back and site.data.links_back.links and site.data.links_back.links.size > 0 %}
{% for item in site.data.links_back.links %}
<div class="source-item">
<a href="{{ item.url }}" target="_blank" rel="noopener">{{ item.name }}</a>
</div>
{% endfor %}
{% else %}
<p>No one listed yet.</p>
{% endif %}
</div>
</div>
