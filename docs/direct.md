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
  cursor: pointer;
}
.source-badge:hover { opacity: 0.85; }
.source-badge--the-pragmatic-engineer { background: #7c3aed; }
.source-badge--bytebytego { background: #0284c7; }
.source-badge--computer-enhance { background: #dc2626; }
.source-badge--julia-evans { background: #059669; }
.source-badge--dan-luu { background: #d97706; }
.source-badge--software-architecture-weekly { background: #6366f1; }
.source-badge--schopenhauer-s-kubernetes-cluster { background: #0891b2; }
.source-badge--indie-developer-diaries { background: #db2777; }
.source-badge--how-tech { background: #9333ea; }

/* Filter bar */
.indie-filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}
.indie-filter-bar .source-badge {
  font-size: 0.75rem;
  padding: 4px 10px;
}
.indie-filter-bar .source-badge.active {
  outline: 2px solid #111;
  outline-offset: 1px;
}
.indie-article.hidden { display: none; }

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

{% assign hero_slug = hero.source | slugify %}
<div class="indie-hero">
  <a href="{{ hero.url }}" target="_blank" rel="noopener" class="hero-badge" style="text-decoration:none;">Today's Indie Pick</a>
  <h2><a href="{{ hero.url }}" target="_blank" rel="noopener">{{ hero.title | escape }}</a></h2>
  <div class="hero-meta">
    {{ hero.date }}
    · <a href="/indie/#{{ hero_slug }}" class="source-badge source-badge--{{ hero_slug }}">{{ hero.source }}</a>
  </div>
  {% if hero.description and hero.description != "" %}
  <p class="hero-desc">{{ hero.description | truncate: 200 }}</p>
  {% endif %}
</div>

<div class="indie-filter-bar" id="indie-filters">
  <a class="source-badge source-badge--the-pragmatic-engineer" data-filter="the-pragmatic-engineer">The Pragmatic Engineer</a>
  <a class="source-badge source-badge--bytebytego" data-filter="bytebytego">ByteByteGo</a>
  <a class="source-badge source-badge--computer-enhance" data-filter="computer-enhance">Computer, Enhance!</a>
  <a class="source-badge source-badge--julia-evans" data-filter="julia-evans">Julia Evans</a>
  <a class="source-badge source-badge--dan-luu" data-filter="dan-luu">Dan Luu</a>
  <a class="source-badge source-badge--software-architecture-weekly" data-filter="software-architecture-weekly">Software Architecture Weekly</a>
  <a class="source-badge source-badge--schopenhauer-s-kubernetes-cluster" data-filter="schopenhauer-s-kubernetes-cluster">Schopenhauer's K8s</a>
  <a class="source-badge source-badge--indie-developer-diaries" data-filter="indie-developer-diaries">Indie Developer Diaries</a>
  <a class="source-badge source-badge--how-tech" data-filter="how-tech">How Tech</a>
</div>

{% for art in site.data.direct_articles.articles offset:1 %}
{% assign src_slug = art.source | slugify %}
<article class="post-item indie-article" data-source="{{ src_slug }}">
  <h2 class="post-title">
    <a href="{{ art.url }}" target="_blank" rel="noopener">{{ art.title | escape }}</a>
  </h2>
  <div class="post-meta">
    {{ art.date }}
    · {{ art.source }}
    · <a href="/indie/#{{ src_slug }}" class="source-badge source-badge--{{ src_slug }}">{{ art.source }}</a>
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

<script>
(function() {
  var filters = document.getElementById('indie-filters');
  if (!filters) return;
  var articles = document.querySelectorAll('.indie-article');
  var hero = document.querySelector('.indie-hero');
  var active = null;

  function applyHash() {
    var h = location.hash.replace('#', '');
    if (h) toggle(h); else showAll();
  }

  function toggle(slug) {
    if (active === slug) { showAll(); return; }
    active = slug;
    articles.forEach(function(a) {
      a.classList.toggle('hidden', a.getAttribute('data-source') !== slug);
    });
    if (hero) hero.style.display = 'none';
    filters.querySelectorAll('.source-badge').forEach(function(b) {
      b.classList.toggle('active', b.getAttribute('data-filter') === slug);
    });
  }

  function showAll() {
    active = null;
    articles.forEach(function(a) { a.classList.remove('hidden'); });
    if (hero) hero.style.display = '';
    filters.querySelectorAll('.source-badge').forEach(function(b) { b.classList.remove('active'); });
    history.replaceState(null, '', location.pathname);
  }

  filters.addEventListener('click', function(e) {
    var btn = e.target.closest('[data-filter]');
    if (!btn) return;
    e.preventDefault();
    var slug = btn.getAttribute('data-filter');
    if (active === slug) showAll();
    else { location.hash = slug; toggle(slug); }
  });

  document.querySelectorAll('.post-meta .source-badge').forEach(function(a) {
    a.addEventListener('click', function(e) {
      e.preventDefault();
      var slug = this.classList.toString().match(/source-badge--([^\s]+)/);
      if (slug) { location.hash = slug[1]; toggle(slug[1]); }
    });
  });

  applyHash();
  window.addEventListener('hashchange', applyHash);
})();
</script>
