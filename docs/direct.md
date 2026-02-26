---
layout: default
title: Direct
description: "Developers and newsletters we link to directly — to their site, not to a platform. We link to you; link back if you like."
permalink: /direct/
---

<style>
.direct-page h1 { font-size: 1.5rem; margin-bottom: 0.25rem; font-family: 'JetBrains Mono', monospace; }
.direct-page .lead { color: #666; font-size: 0.95rem; line-height: 1.6; margin-bottom: 1rem; }
.direct-page .weirdo { color: #555; font-size: 0.9rem; line-height: 1.5; margin-bottom: 2rem; }
.direct-page .link-list { display: grid; gap: 0.75rem; }
.direct-page .link-item {
  display: flex; flex-wrap: wrap; align-items: baseline; gap: 0.5rem;
  padding: 0.75rem 1rem; background: #fafafa; border: 1px solid #e5e5e5; border-radius: 8px;
}
.direct-page .link-item:hover { border-color: #ccc; background: #fff; }
.direct-page .link-name { font-weight: 600; }
.direct-page .link-name a { color: #111; text-decoration: none; }
.direct-page .link-name a:hover { color: #0066cc; }
.direct-page .link-url { font-size: 0.85rem; }
.direct-page .link-url a { color: #0066cc; text-decoration: none; }
.direct-page .link-url a:hover { text-decoration: underline; }
.direct-page .link-desc { width: 100%; font-size: 0.85rem; color: #666; margin-top: 0.25rem; }
.direct-page .cta { margin-top: 2rem; padding: 1rem; background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; font-size: 0.9rem; color: #0c4a6e; }
.direct-page .cta a { color: #0369a1; font-weight: 500; }
</style>

<div class="direct-page">

# Direct

<p class="lead">We link to developers and newsletters directly — to their site, not to a platform.</p>

<p class="weirdo">Indie devs, personal blogs, low-level tinkerers, game devs — we link to you. Got a blog or project? <a href="/about/">Get in touch</a> to be listed.</p>

{% if site.data.direct_links.links and site.data.direct_links.links.size > 0 %}
<div class="link-list">
{% for item in site.data.direct_links.links %}
<div class="link-item">
  <span class="link-name"><a href="{{ item.url }}" target="_blank" rel="noopener">{{ item.name }}</a></span>
  <span class="link-url"><a href="{{ item.url }}" target="_blank" rel="noopener">{{ item.url }}</a></span>
  {% if item.description %}
  <p class="link-desc">{{ item.description }}</p>
  {% endif %}
</div>
{% endfor %}
</div>
{% else %}
<p>No direct links yet. Add entries to <code>DIRECT_LINKS</code> in <code>const.py</code> and run <code>python main.py --action direct</code> (or the news pipeline) to generate the list.</p>
{% endif %}

<div class="cta">
  <strong>We link to you.</strong> Want to be listed or link back? Add “As seen on <a href="/">eof.news</a>” or link to this page from your site. <a href="/about/">Get in touch</a>.
</div>

<p style="margin-top:2rem; font-size:0.9rem; color:#666;"><a href="/">← Home</a> · <a href="/sources/">Sources</a></p>

</div>
