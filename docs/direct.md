---
layout: base
title: Indie | eof.news
description: "Recent articles from indie developers and newsletters. Links to articles, not sites."
permalink: /indie/
---

<style>
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
.post-title a {
  color: #111;
  text-decoration: none;
}
.post-title a:hover {
  color: #0066cc;
}
.post-meta {
  font-size: 0.8rem;
  color: #888;
  margin-bottom: 0.5rem;
}
.indie-links-back {
  margin-top: 2.5rem;
}
.indie-links-back h2 {
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #eee;
}
.indie-links-back p.sub {
  color: #666;
  font-size: 0.85rem;
  margin-bottom: 1rem;
}
.indie-links-back .source-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 0.75rem;
}
.indie-links-back .source-item {
  background: #fafafa;
  border: 1px solid #e5e5e5;
  border-radius: 6px;
  padding: 1rem;
}
.indie-links-back .source-item a {
  color: #111;
  text-decoration: none;
  font-weight: 500;
}
.indie-links-back .source-item a:hover {
  color: #0066cc;
}
</style>

{% if site.data.direct_articles and site.data.direct_articles.articles and site.data.direct_articles.articles.size > 0 %}
{% for art in site.data.direct_articles.articles %}
<article class="post-item">
  <h2 class="post-title">
    <a href="{{ art.url }}" target="_blank" rel="noopener">{{ art.title | escape }}</a>
  </h2>
  <div class="post-meta">
    {{ art.date }} · {{ art.source }}
  </div>
</article>
{% endfor %}
{% else %}
<p>No articles yet.</p>
{% endif %}

<div class="indie-links-back">
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
