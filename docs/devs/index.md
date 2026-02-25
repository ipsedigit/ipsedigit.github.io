---
layout: base
title: "Featured Developers — eof.news"
description: "Indie developers, newsletter authors, and engineering thought leaders featured on eof.news. Real people building real things."
permalink: /devs/
---

<style>
.devs-page h1 { font-size: 1.5rem; margin-bottom: 0.25rem; }
.devs-page .lead { color: #666; font-size: 0.95rem; line-height: 1.6; margin-bottom: 2rem; }
.devs-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }
.dev-card {
  background: #fafafa; border: 1px solid #e5e5e5; border-radius: 8px; padding: 1.25rem;
  transition: border-color 0.2s;
}
.dev-card:hover { border-color: #999; }
.dev-card-name { font-weight: 600; font-size: 1rem; margin: 0 0 0.25rem 0; }
.dev-card-name a { color: #111; text-decoration: none; }
.dev-card-name a:hover { color: #0066cc; }
.dev-card-bio { color: #666; font-size: 0.85rem; line-height: 1.5; margin: 0 0 0.5rem 0; }
.dev-card-url { font-size: 0.8rem; }
.dev-card-url a { color: #0066cc; text-decoration: none; }
.dev-card-url a:hover { text-decoration: underline; }
.dev-card-meta { font-size: 0.75rem; color: #aaa; margin-top: 0.5rem; }
</style>

<div class="devs-page">

# Featured Developers

<p class="lead">
Indie developers, newsletter authors, and engineering thought leaders we curate from.
We monitor their feeds and feature their best work on eof.news.
Each profile links directly to their blog — no platform intermediation.
</p>

{% if site.data.devs.devs and site.data.devs.devs.size > 0 %}
<div class="devs-grid">
{% for dev in site.data.devs.devs %}
<div class="dev-card">
  <p class="dev-card-name"><a href="/devs/{{ dev.slug }}/">{{ dev.name }}</a></p>
  <p class="dev-card-bio">{{ dev.bio }}</p>
  <p class="dev-card-url"><a href="{{ dev.url }}" target="_blank" rel="noopener">{{ dev.url }}</a></p>
  <p class="dev-card-meta">Featured since {{ dev.featured_since }}</p>
</div>
{% endfor %}
</div>
{% else %}
<p>No featured developers yet. Run the news pipeline to generate profiles.</p>
{% endif %}

<p style="margin-top:2rem; font-size:0.9rem; color:#666;">
  Are you an indie developer or newsletter author? <a href="/about/">Get in touch</a> to be featured.
</p>

</div>
