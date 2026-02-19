---
layout: default
title: eof.news — Daily AI & Security Intelligence
description: "One carefully selected AI or security story, every day. No noise, just signal."
keywords: "ai news, cybersecurity news, daily ai digest, security intelligence, artificial intelligence"
---

<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
* { box-sizing: border-box; }

body {
  background: #fff !important;
  color: #111 !important;
  font-family: 'JetBrains Mono', monospace !important;
  line-height: 1.6;
  font-size: 14px;
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

/* ---- Hero ---- */
.hero {
  margin-bottom: 2.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #111;
}
.hero h1 {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0 0 0.25rem 0;
  letter-spacing: -0.5px;
}
.hero p {
  color: #555;
  margin: 0 0 1rem 0;
  font-size: 0.95rem;
}
.hero-nav {
  display: flex;
  gap: 1.5rem;
  font-size: 0.85rem;
}
.hero-nav a {
  color: #444;
  text-decoration: none;
  border-bottom: 1px solid #ccc;
  padding-bottom: 1px;
}
.hero-nav a:hover { color: #000; border-color: #000; }

/* ---- Category section ---- */
.category-section {
  margin-bottom: 3rem;
}
.category-header {
  display: flex;
  align-items: baseline;
  gap: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e5e5e5;
}
.category-title {
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0;
}
.category-label-ai    { color: #0055ff; }
.category-label-sec   { color: #cc0000; }
.category-label-digest{ color: #007700; }

.category-desc {
  font-size: 0.8rem;
  color: #888;
  margin: 0;
}
.category-viewall {
  margin-left: auto;
  font-size: 0.8rem;
  color: #888;
  text-decoration: none;
}
.category-viewall:hover { color: #111; }

/* ---- Post card ---- */
.post-item {
  padding: 1rem 1.1rem;
  margin-bottom: 0.75rem;
  border: 1px solid #e5e5e5;
  border-radius: 6px;
  background: #fafafa;
  transition: border-color 0.15s;
}
.post-item:hover { border-color: #bbb; background: #f5f5f5; }

.post-title {
  margin: 0 0 0.35rem 0;
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.4;
}
.post-title a {
  color: #111;
  text-decoration: none;
}
.post-title a:hover { color: #0055ff; }

.post-meta {
  font-size: 0.78rem;
  color: #999;
  margin-bottom: 0.35rem;
}
.post-meta .source { color: #666; }

.post-tags { display: inline; }
.post-tags a {
  color: #888;
  text-decoration: none;
  font-size: 0.78rem;
}
.post-tags a::before { content: "#"; }
.post-tags a + a { margin-left: 0.4rem; }
.post-tags a:hover { color: #0055ff; }

.post-preview {
  color: #555;
  font-size: 0.88rem;
  margin: 0.4rem 0 0 0;
  line-height: 1.5;
}

/* ---- Digest card (slightly different) ---- */
.post-item.digest {
  border-left: 3px solid #007700;
}

/* ---- Ad ---- */
.ad-space {
  background: #fafafa;
  border: 1px solid #eee;
  padding: 1rem;
  margin: 2rem 0;
  text-align: center;
  min-height: 90px;
}

/* ---- Empty state ---- */
.empty-state {
  color: #aaa;
  font-size: 0.85rem;
  padding: 0.75rem 0;
}
</style>

<!-- ================================================================== -->
<!-- HERO -->
<!-- ================================================================== -->

<div class="hero">
  <h1>eof.news</h1>
  <p>One carefully selected AI or security story, every day. No noise, just signal.</p>
  <div class="hero-nav">
    <a href="#ai">🤖 AI</a>
    <a href="#security">🔐 Security</a>
    <a href="#digest">📋 Weekly Digest</a>
    <a href="/feed.xml">RSS</a>
  </div>
</div>

<div class="ad-space">
  {% if site.adsense_id %}
  <ins class="adsbygoogle" style="display:block"
    data-ad-client="{{ site.adsense_id }}"
    data-ad-slot="TOP"
    data-ad-format="auto"
    data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  {% endif %}
</div>

<!-- ================================================================== -->
<!-- AI SECTION -->
<!-- ================================================================== -->

{% assign ai_posts = site.posts | where: "niche_category", "ai" %}

<section class="category-section" id="ai">
  <div class="category-header">
    <h2 class="category-title category-label-ai">🤖 Artificial Intelligence</h2>
    <span class="category-desc">Research, models, and industry moves</span>
    {% if ai_posts.size > 6 %}
    <a class="category-viewall" href="/tags/ai/">View all →</a>
    {% endif %}
  </div>

  {% if ai_posts.size == 0 %}
  <p class="empty-state">No AI posts yet — check back soon.</p>
  {% else %}
  {% for post in ai_posts limit: 6 %}
  <article class="post-item">
    <h3 class="post-title">
      {% if post.external_url %}
      <a href="{{ post.external_url }}" target="_blank" rel="noopener">{{ post.title }}</a>
      {% else %}
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      {% endif %}
    </h3>
    <div class="post-meta">
      {{ post.date | date: "%b %d, %Y" }}
      {% if post.source %}<span class="source"> · {{ post.source }}</span>{% endif %}
      {% if post.reading_time %} · {{ post.reading_time }} min read{% endif %}
      {% if post.categories.size > 0 %}
       · <span class="post-tags">
        {% for category in post.categories limit: 3 %}
        <a href="/tags/{{ category | slugify: 'latin' }}/">{{ category }}</a>
        {% endfor %}
      </span>
      {% endif %}
    </div>
    {% if post.description %}
    <p class="post-preview">{{ post.description | truncate: 160 }}</p>
    {% endif %}
  </article>
  {% endfor %}
  {% endif %}
</section>

<div class="ad-space">
  {% if site.adsense_id %}
  <ins class="adsbygoogle" style="display:block"
    data-ad-client="{{ site.adsense_id }}"
    data-ad-slot="MID"
    data-ad-format="auto"
    data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  {% endif %}
</div>

<!-- ================================================================== -->
<!-- SECURITY SECTION -->
<!-- ================================================================== -->

{% assign sec_posts = site.posts | where: "niche_category", "security" %}

<section class="category-section" id="security">
  <div class="category-header">
    <h2 class="category-title category-label-sec">🔐 Security</h2>
    <span class="category-desc">Breaches, vulnerabilities, and threat intelligence</span>
    {% if sec_posts.size > 6 %}
    <a class="category-viewall" href="/tags/security/">View all →</a>
    {% endif %}
  </div>

  {% if sec_posts.size == 0 %}
  <p class="empty-state">No security posts yet — check back soon.</p>
  {% else %}
  {% for post in sec_posts limit: 6 %}
  <article class="post-item">
    <h3 class="post-title">
      {% if post.external_url %}
      <a href="{{ post.external_url }}" target="_blank" rel="noopener">{{ post.title }}</a>
      {% else %}
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      {% endif %}
    </h3>
    <div class="post-meta">
      {{ post.date | date: "%b %d, %Y" }}
      {% if post.source %}<span class="source"> · {{ post.source }}</span>{% endif %}
      {% if post.reading_time %} · {{ post.reading_time }} min read{% endif %}
      {% if post.categories.size > 0 %}
       · <span class="post-tags">
        {% for category in post.categories limit: 3 %}
        <a href="/tags/{{ category | slugify: 'latin' }}/">{{ category }}</a>
        {% endfor %}
      </span>
      {% endif %}
    </div>
    {% if post.description %}
    <p class="post-preview">{{ post.description | truncate: 160 }}</p>
    {% endif %}
  </article>
  {% endfor %}
  {% endif %}
</section>

<!-- ================================================================== -->
<!-- WEEKLY DIGEST SECTION -->
<!-- ================================================================== -->

{% assign digest_posts = site.posts | where: "niche_category", "digest" %}

<section class="category-section" id="digest">
  <div class="category-header">
    <h2 class="category-title category-label-digest">📋 Weekly Digest</h2>
    <span class="category-desc">Top 5 AI & security stories, every Sunday</span>
  </div>

  {% if digest_posts.size == 0 %}
  <p class="empty-state">First digest coming Sunday.</p>
  {% else %}
  {% for post in digest_posts limit: 3 %}
  <article class="post-item digest">
    <h3 class="post-title">
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </h3>
    <div class="post-meta">
      {{ post.date | date: "%b %d, %Y" }}
    </div>
    {% if post.description %}
    <p class="post-preview">{{ post.description | truncate: 160 }}</p>
    {% endif %}
  </article>
  {% endfor %}
  {% endif %}
</section>

<div class="ad-space">
  {% if site.adsense_id %}
  <ins class="adsbygoogle" style="display:block"
    data-ad-client="{{ site.adsense_id }}"
    data-ad-slot="BOTTOM"
    data-ad-format="auto"
    data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  {% endif %}
</div>
