---
layout: base
title: Direct | eof.news
description: "We link to developers directly — to your site, not to a platform. So you know we're linking; link back if you like. We list who links to us."
permalink: /direct/
---

<style>
.direct-page h1 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  font-family: 'JetBrains Mono', monospace;
}
.direct-page > p {
  color: #666;
  margin-bottom: 2rem;
  font-size: 0.9rem;
  line-height: 1.6;
}
.direct-page .source-category {
  margin-bottom: 2.5rem;
}
.direct-page .source-category h2 {
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #eee;
}
.direct-page .source-category p.sub {
  color: #666;
  font-size: 0.85rem;
  margin-bottom: 1rem;
  line-height: 1.5;
}
.direct-page .source-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 0.75rem;
}
.direct-page .source-item {
  background: #fafafa;
  border: 1px solid #e5e5e5;
  border-radius: 6px;
  padding: 1rem;
  transition: all 0.2s;
}
.direct-page .source-item:hover {
  border-color: #999;
  background: #fff;
}
.direct-page .source-item a {
  color: #111;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
}
.direct-page .source-item a:hover {
  color: #0066cc;
}
.direct-page .source-item p {
  color: #666;
  font-size: 0.8rem;
  margin: 0.5rem 0 0 0;
  line-height: 1.4;
}
.direct-page .source-item .type {
  display: inline-block;
  background: #e5e5e5;
  color: #666;
  font-size: 0.7rem;
  padding: 2px 6px;
  border-radius: 3px;
  margin-top: 0.5rem;
}
.direct-page .footer-links {
  margin-top: 2rem;
  font-size: 0.9rem;
  color: #666;
}
.direct-page .footer-links a {
  color: #0066cc;
  text-decoration: none;
}
.direct-page .footer-links a:hover {
  text-decoration: underline;
}
</style>

<div class="direct-page">

# Direct

<p>We refer to a single list of weirdo developers (indie, offbeat, worldwide) and link to them directly — to your site, not to a platform — so you know we're linking and can link back if you like. We track who links to us and list them below.</p>

<div class="source-category">
<h2>We link to you</h2>
<p class="sub">Each link goes to your site. Indie devs, personal blogs, low-level tinkerers — we link to you. Want to be listed? <a href="/about/">Get in touch</a>.</p>
<div class="source-list">
{% if site.data.direct_links.links and site.data.direct_links.links.size > 0 %}
{% for item in site.data.direct_links.links %}
<div class="source-item">
<a href="{{ item.url }}" target="_blank" rel="noopener">{{ item.name }}</a>
{% if item.description %}
<p>{{ item.description }}</p>
{% endif %}
<span class="type">Direct</span>
</div>
{% endfor %}
{% else %}
<p>No direct links yet. Add entries to the reference list (<code>DIRECT_REFERENCE_LIST</code>) in <code>const.py</code> and run <code>python main.py --action direct</code>.</p>
{% endif %}
</div>
</div>

<div class="source-category">
<h2>Who links to us</h2>
<p class="sub">Sites that link back to eof.news. If you link to us, <a href="/about/">tell us</a> and we'll add you here.</p>
<div class="source-list">
{% if site.data.links_back.links and site.data.links_back.links.size > 0 %}
{% for item in site.data.links_back.links %}
<div class="source-item">
<a href="{{ item.url }}" target="_blank" rel="noopener">{{ item.name }}</a>
{% if item.description %}
<p>{{ item.description }}</p>
{% endif %}
<span class="type">Links back</span>
</div>
{% endfor %}
{% else %}
<p>No one listed yet. When we discover or you tell us you link to eof.news, we add you here.</p>
{% endif %}
</div>
</div>

<p class="footer-links"><a href="/">Home</a> · <a href="/sources/">Sources</a> · <a href="/about/">Get in touch</a></p>

</div>
