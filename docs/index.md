---
layout: default
title: ipsedigit - Daily Curated Tech News from Hacker News
description: "Daily curated tech news from Hacker News. AI, Machine Learning, Programming, Cloud Computing, DevOps, and Software Engineering trends and insights."
keywords: "tech news, hacker news, programming, AI, machine learning, software engineering, devops, cloud computing"
---

<style>
:root {
  --terminal-green: #16a34a;
  --terminal-dim: #22c55e;
  --bg-light: #ffffff;
  --bg-card: #f8fafc;
  --bg-code: #f1f5f9;
  --text-main: #1e293b;
  --text-dim: #64748b;
  --border: #e2e8f0;
  --accent: #2563eb;
  --accent-hover: #1d4ed8;
}

body {
  background: var(--bg-light) !important;
  color: var(--text-main) !important;
}

.page-content {
  background: var(--bg-light) !important;
}

/* Header nerd style */
.site-header {
  background: var(--bg-card) !important;
  border-bottom: 2px solid var(--terminal-green) !important;
}

.site-title, .site-title:visited {
  color: var(--terminal-green) !important;
  font-family: 'Courier New', monospace !important;
  letter-spacing: 2px;
}

.site-title::before {
  content: "> ";
  color: var(--terminal-dim);
}

/* Navigation */
.site-nav .page-link {
  color: var(--text-main) !important;
}

.site-nav .page-link:hover {
  color: var(--terminal-green) !important;
}

/* Ad Banner */
.ad-banner {
  background: var(--bg-code);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 1rem;
  margin: 1.5rem 0;
  text-align: center;
  min-height: 90px;
}

.ad-banner-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-dim);
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  min-height: 90px;
}

/* Support Banner */
.support-banner {
  background: linear-gradient(135deg, var(--terminal-green), var(--accent));
  color: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 2rem 0;
  text-align: center;
}

.support-banner h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.support-banner p {
  margin: 0 0 1rem 0;
  opacity: 0.9;
  font-size: 0.9rem;
}

.support-banner a {
  display: inline-block;
  background: white;
  color: var(--terminal-green);
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  text-decoration: none;
  font-weight: 600;
  transition: transform 0.2s;
}

.support-banner a:hover {
  transform: scale(1.05);
}

/* Post Item */
.post-item {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px;
  margin-bottom: 1.25rem;
  padding: 1.25rem;
  transition: box-shadow 0.2s;
}

.post-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* Post Header - Titolo + Tags sulla stessa riga o wrappati */
.post-header {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 0.5rem 1rem;
  margin-bottom: 0.5rem;
}

/* Post Title - Link diretto all'articolo esterno */
.post-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  line-height: 1.4;
  flex: 1 1 auto;
  min-width: 200px;
}

.post-title a {
  color: var(--text-main);
  text-decoration: none;
}

.post-title a:hover {
  color: var(--accent);
  text-decoration: underline;
}

/* Tags inline */
.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.post-tags a {
  background: var(--bg-code);
  color: var(--terminal-green);
  padding: 2px 8px;
  border-radius: 3px;
  text-decoration: none;
  font-size: 0.7rem;
  font-family: 'Courier New', monospace;
  border: 1px solid var(--border);
  transition: all 0.2s;
}

.post-tags a:hover {
  background: var(--terminal-green);
  color: white;
  border-color: var(--terminal-green);
}

/* Post Meta - Data e fonte */
.post-meta {
  font-size: 0.8rem;
  color: var(--text-dim);
  margin-bottom: 0.75rem;
}

/* Post Preview */
.post-preview {
  color: var(--text-dim);
  font-size: 0.9rem;
  line-height: 1.6;
  margin: 0;
}

.post-preview img {
  max-width: 100%;
  border-radius: 6px;
  margin-top: 0.75rem;
  border: 1px solid var(--border);
}

.post-preview-img {
  max-width: 100%;
  max-height: 200px;
  object-fit: cover;
  border-radius: 6px;
  margin-top: 0.75rem;
  border: 1px solid var(--border);
}

/* Footer */
}

.post-excerpt blockquote::before {
  content: "// ";
  color: var(--terminal-dim);
}

/* Footer */
.site-footer {
  background: var(--bg-card) !important;
  border-top: 2px solid var(--terminal-green) !important;
  color: var(--text-dim) !important;
}

.site-footer a {
  color: var(--terminal-green) !important;
}


/* Responsive */
@media (max-width: 600px) {
  .post-item {
    padding: 1rem;
  }
  .post-title {
    font-size: 1.1rem;
  }
  .ad-banner {
    min-height: 60px;
  }
}
</style>

<!-- Support Banner -->
<div class="support-banner">
  <h3>☕ Enjoy this curated tech news?</h3>
  <p>Help keep this site running and ad-free for everyone</p>
  {% if site.buymeacoffee %}
  <a href="https://www.buymeacoffee.com/{{ site.buymeacoffee }}" target="_blank">Buy me a coffee</a>
  {% elsif site.kofi %}
  <a href="https://ko-fi.com/{{ site.kofi }}" target="_blank">Support on Ko-fi</a>
  {% else %}
  <a href="https://github.com/{{ site.github_username }}" target="_blank">⭐ Star on GitHub</a>
  {% endif %}
</div>

<!-- Top Ad Banner -->
<div class="ad-banner" id="ad-top">
  {% if site.adsense_id %}
  <ins class="adsbygoogle"
       style="display:block"
       data-ad-client="{{ site.adsense_id }}"
       data-ad-slot="TOP_AD_SLOT"
       data-ad-format="horizontal"
       data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  {% else %}
  <div class="ad-banner-placeholder">// Sponsored content coming soon</div>
  {% endif %}
</div>

{% assign post_count = 0 %}
{% for post in site.posts %}

{% assign post_count = post_count | plus: 1 %}

<article class="post-item">
  <div class="post-header">
    <h2 class="post-title">
      {% if post.external_url %}
      <a href="{{ post.external_url }}" target="_blank" rel="noopener">{{ post.title }}</a>
      {% else %}
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      {% endif %}
    </h2>
    <span class="post-tags">
      {% for category in post.categories %}
        {% assign tag_slug = category | slugify: "latin" %}
        <a href="/tags/{{ tag_slug }}/">{{ category }}</a>
      {% endfor %}
    </span>
  </div>
  <div class="post-meta">{{ post.date | date: "%Y-%m-%d" }}{% if post.source %} · {{ post.source }}{% endif %}</div>
  {% if post.description %}
  <p class="post-preview">{{ post.description }}</p>
  {% endif %}
  {% if post.image %}
  <img src="{{ post.image }}" alt="{{ post.title }}" class="post-preview-img" loading="lazy">
  {% endif %}
</article>

{% assign mod = post_count | modulo: 5 %}
{% if mod == 0 %}
<div class="ad-banner" id="ad-mid-{{ post_count }}">
  {% if site.adsense_id %}
  <ins class="adsbygoogle"
       style="display:block"
       data-ad-client="{{ site.adsense_id }}"
       data-ad-slot="MID_AD_SLOT"
       data-ad-format="auto"
       data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  {% endif %}
</div>
{% endif %}

{% endfor %}

<!-- Bottom Ad Banner -->
<div class="ad-banner" id="ad-bottom">
  {% if site.adsense_id %}
  <ins class="adsbygoogle"
       style="display:block"
       data-ad-client="{{ site.adsense_id }}"
       data-ad-slot="BOTTOM_AD_SLOT"
       data-ad-format="auto"
       data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  {% else %}
  <div class="ad-banner-placeholder">// Sponsored content coming soon</div>
  {% endif %}
</div>

