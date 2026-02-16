---
layout: default
title: TechPulse Daily - The Smartest Tech News Digest
description: "The smartest tech news digest. AI, startups, programming, and engineering insights curated daily from top sources. No noise, just signal."
keywords: "tech news, AI news, startup news, programming, software engineering, hacker news, tech digest"
---

<style>
:root {
  --primary: #6366f1;
  --primary-dark: #4f46e5;
  --accent: #f59e0b;
  --bg: #ffffff;
  --bg-alt: #f8fafc;
  --text: #0f172a;
  --text-secondary: #64748b;
  --border: #e2e8f0;
  --success: #10b981;
}

* { box-sizing: border-box; }

body {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}

.page-content { background: var(--bg) !important; }

.site-header {
  background: var(--text) !important;
  border: none !important;
}
.site-title, .site-title:visited {
  color: white !important;
  font-weight: 700 !important;
  font-size: 1.4rem !important;
}
.site-nav .page-link { color: rgba(255,255,255,0.8) !important; }
.site-nav .page-link:hover { color: white !important; }

.hero {
  background: linear-gradient(135deg, var(--text) 0%, #1e293b 100%);
  color: white;
  padding: 3rem 1rem;
  margin: -30px -15px 2rem -15px;
  text-align: center;
}
.hero h1 {
  font-size: 2.5rem;
  margin: 0 0 0.5rem 0;
  font-weight: 800;
}
.hero .tagline {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 1.5rem;
}
.hero .stats {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}
.hero .stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: var(--accent);
}
.hero .stat-label {
  font-size: 0.85rem;
  opacity: 0.8;
}

.newsletter-cta {
  background: var(--primary);
  color: white;
  padding: 1.5rem;
  border-radius: 12px;
  margin: 2rem 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}
.newsletter-cta h3 { margin: 0; font-size: 1.1rem; }
.newsletter-cta p { margin: 0.25rem 0 0 0; opacity: 0.9; font-size: 0.9rem; }
.newsletter-cta .btn {
  background: white;
  color: var(--primary);
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: transform 0.2s;
}
.newsletter-cta .btn:hover { transform: scale(1.05); }

.section-header {
  display: flex;
  align-items: center;
  margin: 2rem 0 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--border);
}
.section-header h2 { margin: 0; font-size: 1.3rem; }

.post-item {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.25rem;
  margin-bottom: 1rem;
  transition: all 0.2s;
}
.post-item:hover {
  border-color: var(--primary);
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.1);
}

.post-header {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  gap: 0.75rem;
}

.post-title {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 600;
  line-height: 1.4;
  flex: 1;
}
.post-title a { color: var(--text); text-decoration: none; }
.post-title a:hover { color: var(--primary); }

.post-tags { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.post-tags a {
  background: var(--bg-alt);
  color: var(--primary);
  padding: 4px 10px;
  border-radius: 20px;
  text-decoration: none;
  font-size: 0.7rem;
  font-weight: 500;
  transition: all 0.2s;
}
.post-tags a:hover { background: var(--primary); color: white; }

.post-meta { font-size: 0.8rem; color: var(--text-secondary); margin: 0.5rem 0; }
.post-meta .source { color: var(--success); font-weight: 500; }

.post-preview { color: var(--text-secondary); font-size: 0.9rem; line-height: 1.6; margin: 0.75rem 0 0 0; }

.post-preview-img {
  width: 100%;
  max-height: 200px;
  object-fit: cover;
  border-radius: 8px;
  margin-top: 1rem;
}

.ad-banner {
  background: var(--bg-alt);
  border: 1px dashed var(--border);
  border-radius: 8px;
  padding: 1rem;
  margin: 1.5rem 0;
  min-height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.site-footer {
  background: var(--text) !important;
  color: rgba(255,255,255,0.7) !important;
  border: none !important;
}
.site-footer a { color: white !important; }

@media (max-width: 600px) {
  .hero h1 { font-size: 1.8rem; }
  .newsletter-cta { flex-direction: column; text-align: center; }
}
</style>

<div class="hero">
  <h1>⚡ TechPulse Daily</h1>
  <p class="tagline">{{ site.tagline | default: "Your daily dose of tech that matters" }}</p>
  <div class="stats">
    <div class="stat">
      <div class="stat-number">{{ site.posts | size }}+</div>
      <div class="stat-label">Articles</div>
    </div>
    <div class="stat">
      <div class="stat-number">10+</div>
      <div class="stat-label">Sources</div>
    </div>
    <div class="stat">
      <div class="stat-number">3x</div>
      <div class="stat-label">Daily</div>
    </div>
  </div>
</div>

<div class="newsletter-cta">
  <div>
    <h3>🚀 Never miss a tech story</h3>
    <p>Get the best articles delivered to your inbox</p>
  </div>
  {% if site.newsletter_url %}
  <a href="{{ site.newsletter_url }}" class="btn" target="_blank">Subscribe Free</a>
  {% else %}
  <a href="https://github.com/{{ site.github_username }}" class="btn" target="_blank">⭐ Follow Us</a>
  {% endif %}
</div>

<div class="ad-banner" id="ad-top">
  {% if site.adsense_id %}
  <ins class="adsbygoogle" style="display:block" data-ad-client="{{ site.adsense_id }}" data-ad-slot="TOP" data-ad-format="horizontal" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  {% endif %}
</div>

<div class="section-header">
  <h2>🔥 Latest Tech News</h2>
</div>

{% assign post_count = 0 %}
{% for post in site.posts %}
{% assign post_count = post_count | plus: 1 %}

<article class="post-item">
  <div class="post-header">
    <h3 class="post-title">
      {% if post.external_url %}
      <a href="{{ post.external_url }}" target="_blank" rel="noopener">{{ post.title }}</a>
      {% else %}
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      {% endif %}
    </h3>
    <span class="post-tags">
      {% for category in post.categories %}
      {% assign tag_slug = category | slugify: "latin" %}
      <a href="/tags/{{ tag_slug }}/">{{ category }}</a>
      {% endfor %}
    </span>
  </div>
  <div class="post-meta">
    {{ post.date | date: "%b %d, %Y" }}
    {% if post.source %} · <span class="source">{{ post.source }}</span>{% endif %}
  </div>
  {% if post.description %}
  <p class="post-preview">{{ post.description | truncate: 150 }}</p>
  {% endif %}
  {% if post.image %}
  <img src="{{ post.image }}" alt="{{ post.title }}" class="post-preview-img" loading="lazy">
  {% endif %}
</article>

{% assign mod = post_count | modulo: 5 %}
{% if mod == 0 %}
<div class="ad-banner">
  {% if site.adsense_id %}
  <ins class="adsbygoogle" style="display:block" data-ad-client="{{ site.adsense_id }}" data-ad-slot="MID" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  {% endif %}
</div>
{% endif %}

{% endfor %}

<div class="newsletter-cta" style="background: var(--success);">
  <div>
    <h3>💡 Want more tech insights?</h3>
    <p>Follow us for daily updates on AI, startups & engineering</p>
  </div>
  <a href="https://github.com/{{ site.github_username }}" class="btn" style="color: var(--success);" target="_blank">Follow on GitHub</a>
</div>

<div class="ad-banner" id="ad-bottom">
  {% if site.adsense_id %}
  <ins class="adsbygoogle" style="display:block" data-ad-client="{{ site.adsense_id }}" data-ad-slot="BOTTOM" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  {% endif %}
</div>
