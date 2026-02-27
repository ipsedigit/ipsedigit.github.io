---
layout: base
title: Indie | eof.news
description: "Recent articles from indie developers and newsletters. Links to articles, not sites."
permalink: /indie/
---

<style>
/* Hero — today's pick */
.indie-hero {
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border: 2px solid #059669;
  border-radius: 8px;
  background: #f0fdf4;
}
.indie-hero .hero-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 0.78em;
  font-weight: bold;
  background: #059669;
  color: #fff;
  margin-bottom: 0.75rem;
}
.indie-hero h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1.3;
}
.indie-hero h2 a { color: #111; text-decoration: none; }
.indie-hero h2 a:hover { color: #0066cc; }
.indie-hero .hero-meta {
  font-size: 0.8rem;
  color: #888;
  margin-bottom: 0.5rem;
}
.indie-hero .hero-desc {
  color: #374151;
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0;
}

/* Post cards — same as Home */
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
.post-title a:hover { color: #0066cc; }
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

/* Source badge (colored chip) */
.source-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 600;
  color: #fff;
  text-decoration: none;
}
.source-badge--pragmatic { background: #7c3aed; }
.source-badge--bytebytego { background: #0284c7; }
.source-badge--computerenhance { background: #dc2626; }
.source-badge--juliaevans { background: #059669; }
.source-badge--danluu { background: #d97706; }
.source-badge--archweekly { background: #6366f1; }
.source-badge--strlen { background: #0891b2; }
.source-badge--indiediaries { background: #db2777; }
.source-badge--howtech { background: #9333ea; }
.source-badge--default { background: #6b7280; }

/* Links-back section */
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

{% assign hero = site.data.direct_articles.articles | first %}

<div class="indie-hero">
  <span class="hero-badge">Today's Indie Pick</span>
  <h2><a href="{{ hero.url }}" target="_blank" rel="noopener">{{ hero.title | escape }}</a></h2>
  <div class="hero-meta">
    {{ hero.date }}
    · {{ hero.source }}
  </div>
  {% if hero.description and hero.description != "" %}
  <p class="hero-desc">{{ hero.description | truncate: 200 }}</p>
  {% endif %}
</div>

{% for art in site.data.direct_articles.articles offset:1 %}
<article class="post-item">
  <h2 class="post-title">
    <a href="{{ art.url }}" target="_blank" rel="noopener">{{ art.title | escape }}</a>
  </h2>
  <div class="post-meta">
    {{ art.date }}
    · {{ art.source }}
    · {% if art.source == "The Pragmatic Engineer" %}<span class="source-badge source-badge--pragmatic">{{ art.source }}</span>
    {% elsif art.source == "ByteByteGo" %}<span class="source-badge source-badge--bytebytego">{{ art.source }}</span>
    {% elsif art.source == "Computer, Enhance!" %}<span class="source-badge source-badge--computerenhance">{{ art.source }}</span>
    {% elsif art.source == "Julia Evans" %}<span class="source-badge source-badge--juliaevans">{{ art.source }}</span>
    {% elsif art.source == "Dan Luu" %}<span class="source-badge source-badge--danluu">{{ art.source }}</span>
    {% elsif art.source == "Software Architecture Weekly" %}<span class="source-badge source-badge--archweekly">{{ art.source }}</span>
    {% elsif art.source contains "Schopenhauer" %}<span class="source-badge source-badge--strlen">{{ art.source }}</span>
    {% elsif art.source == "Indie Developer Diaries" %}<span class="source-badge source-badge--indiediaries">{{ art.source }}</span>
    {% elsif art.source == "How Tech" %}<span class="source-badge source-badge--howtech">{{ art.source }}</span>
    {% else %}<span class="source-badge source-badge--default">{{ art.source }}</span>
    {% endif %}
  </div>
  {% if art.description and art.description != "" %}
  <p class="post-preview">{{ art.description | truncate: 160 }}</p>
  {% endif %}
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
