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
  border-left: 3px solid var(--terminal-green);
  border-radius: 6px;
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.post-item:hover {
  border-left-color: var(--accent);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* Post Meta */
.post-meta {
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  color: var(--text-dim);
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.post-meta time {
  color: var(--terminal-green);
}

.post-meta time::before {
  content: "📅 ";
}

/* Tags */
.post-tags a {
  background: var(--bg-code);
  color: var(--terminal-green);
  padding: 2px 8px;
  border-radius: 3px;
  text-decoration: none;
  font-size: 0.75rem;
  border: 1px solid var(--terminal-dim);
  transition: all 0.2s;
}

.post-tags a:hover {
  background: var(--terminal-green);
  color: white;
  border-color: var(--terminal-green);
}

/* Post Title */
.post-title {
  margin: 0.75rem 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.post-title a {
  color: var(--text-main);
  text-decoration: none;
  transition: color 0.2s;
}

.post-title a:hover {
  color: var(--accent);
}

.post-title a::before {
  content: "$ ";
  color: var(--terminal-dim);
  font-family: 'Courier New', monospace;
}

/* Post Content */
.post-excerpt {
  color: var(--text-dim);
  line-height: 1.7;
  font-size: 0.95rem;
}

.post-excerpt h3 {
  margin: 0;
  font-size: 1rem;
}

.post-excerpt h3 a {
  color: var(--accent);
  text-decoration: none;
}

.post-excerpt h3 a:hover {
  text-decoration: underline;
}

.post-excerpt img {
  max-width: 100%;
  border-radius: 6px;
  margin: 1rem 0;
  border: 1px solid var(--border);
}

.post-excerpt blockquote {
  border-left: 3px solid var(--terminal-green);
  background: var(--bg-code);
  margin: 1rem 0;
  padding: 1rem;
  border-radius: 0 6px 6px 0;
  color: var(--text-main);
  font-style: normal;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
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
  <div class="post-meta">
    <time>{{ post.date | date: "%Y-%m-%d" }}</time>
    <span class="post-tags">
      {% for category in post.categories %}
        {% assign tag_slug = category | slugify: "latin" %}
        {% capture tag_url %}/tags/{{ tag_slug }}/{% endcapture %}
        <a href="{{ tag_url }}">{{ category }}</a>
      {% endfor %}
    </span>
  </div>
  <h2 class="post-title">
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
  </h2>
  <div class="post-excerpt">
    {{ post.content }}
  </div>
</article>

{% comment %} Ad ogni 5 post inserisci uno spazio ads {% endcomment %}
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

