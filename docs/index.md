---
layout: default
title: TechPulse Daily - Tech News Digest
description: "The smartest tech news digest. AI, startups, programming, and engineering insights curated daily from top sources."
keywords: "tech news, AI news, startup news, programming, software engineering"
---

<style>
* { box-sizing: border-box; }

body {
  background: #fff !important;
  color: #111 !important;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  line-height: 1.6;
}

.page-content { 
  background: #fff !important; 
  padding-top: 1rem;
}

.site-header {
  background: #fff !important;
  border-bottom: 1px solid #eee !important;
}
.site-title, .site-title:visited {
  color: #111 !important;
  font-weight: 700 !important;
}
.site-nav .page-link { color: #666 !important; }
.site-nav .page-link:hover { color: #111 !important; }

.site-footer {
  background: #fafafa !important;
  border-top: 1px solid #eee !important;
  color: #666 !important;
}
.site-footer a { color: #111 !important; }

/* Header */
.page-header {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}
.page-header h1 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 0.25rem 0;
}
.page-header p {
  color: #666;
  margin: 0;
  font-size: 0.95rem;
}

/* Post */
.post-item {
  padding: 1.25rem 0;
  border-bottom: 1px solid #eee;
}
.post-item:last-child {
  border-bottom: none;
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

.post-tags {
  display: inline;
}
.post-tags a {
  color: #666;
  text-decoration: none;
  font-size: 0.8rem;
}
.post-tags a:hover {
  color: #0066cc;
}
.post-tags a::before {
  content: "#";
}
.post-tags a + a {
  margin-left: 0.5rem;
}

.post-preview {
  color: #444;
  font-size: 0.9rem;
  margin: 0.5rem 0 0 0;
  line-height: 1.5;
}

.post-image {
  margin-top: 0.75rem;
}
.post-image img {
  max-width: 100%;
  max-height: 180px;
  object-fit: cover;
  border-radius: 4px;
}

/* Ad */
.ad-space {
  background: #fafafa;
  border: 1px solid #eee;
  padding: 1rem;
  margin: 1.5rem 0;
  text-align: center;
  min-height: 90px;
}
</style>

<div class="page-header">
  <h1>TechPulse Daily</h1>
  <p>Curated tech news, updated 3x daily</p>
</div>

<div class="ad-space" id="ad-top">
  {% if site.adsense_id %}
  <ins class="adsbygoogle" style="display:block" data-ad-client="{{ site.adsense_id }}" data-ad-slot="TOP" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  {% endif %}
</div>

{% assign post_count = 0 %}
{% for post in site.posts %}
{% assign post_count = post_count | plus: 1 %}

<article class="post-item">
  <h2 class="post-title">
    {% if post.external_url %}
    <a href="{{ post.external_url }}" target="_blank" rel="noopener">{{ post.title }}</a>
    {% else %}
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    {% endif %}
  </h2>
  <div class="post-meta">
    {{ post.date | date: "%b %d, %Y" }}
    {% if post.source %} · {{ post.source }}{% endif %}
    {% if post.categories.size > 0 %}
    · <span class="post-tags">
      {% for category in post.categories %}
      {% assign tag_slug = category | slugify: "latin" %}
      <a href="/tags/{{ tag_slug }}/">{{ category }}</a>
      {% endfor %}
    </span>
    {% endif %}
  </div>
  {% if post.description %}
  <p class="post-preview">{{ post.description | truncate: 160 }}</p>
  {% endif %}
  {% if post.image %}
  <div class="post-image">
    <img src="{{ post.image }}" alt="" loading="lazy">
  </div>
  {% endif %}
</article>

{% assign mod = post_count | modulo: 8 %}
{% if mod == 0 %}
<div class="ad-space">
  {% if site.adsense_id %}
  <ins class="adsbygoogle" style="display:block" data-ad-client="{{ site.adsense_id }}" data-ad-slot="MID" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  {% endif %}
</div>
{% endif %}

{% endfor %}

<div class="ad-space" id="ad-bottom">
  {% if site.adsense_id %}
  <ins class="adsbygoogle" style="display:block" data-ad-client="{{ site.adsense_id }}" data-ad-slot="BOTTOM" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  {% endif %}
</div>
