---
layout: default
title: From creators
description: "Tech from indie creators and newsletters we feature — Substack, Buttondown, and independent voices. Reach engineers who follow people, not just brands."
permalink: /creators/
---

<style>
.creators-page h1 { font-size: 1.5rem; margin-bottom: 0.5rem; font-family: 'JetBrains Mono', monospace; }
.creators-page .lead { color: #666; margin-bottom: 2rem; font-size: 0.95rem; line-height: 1.6; }
.creators-page .source-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1rem; }
.creators-page .source-item {
  background: #fafafa; border: 1px solid #e5e5e5; border-radius: 8px; padding: 1.25rem;
  transition: all 0.2s;
}
.creators-page .source-item:hover { border-color: #999; background: #fff; }
.creators-page .source-item a { color: #111; text-decoration: none; font-weight: 600; }
.creators-page .source-item a:hover { color: #0066cc; }
.creators-page .source-item p { color: #666; font-size: 0.85rem; margin: 0.5rem 0 0 0; line-height: 1.5; }
.creators-page .source-item .badge { display: inline-block; background: #7c3aed; color: #fff; font-size: 0.7rem; padding: 2px 8px; border-radius: 12px; margin-top: 0.5rem; }
.creators-page .recent h2 { font-size: 1.1rem; margin: 2rem 0 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid #eee; }
.creators-page .post-item { padding: 0.75rem 0; border-bottom: 1px solid #f0f0f0; }
.creators-page .post-item:last-child { border-bottom: none; }
.creators-page .post-item a { color: #111; text-decoration: none; }
.creators-page .post-item a:hover { color: #0066cc; }
.creators-page .post-meta { font-size: 0.8rem; color: #888; margin-top: 0.25rem; }
</style>

<div class="creators-page">

# From creators

Tech from **indie creators and newsletters** we feature — Substack, Buttondown, and independent voices. These are practitioners and thought leaders, not corporate blogs; following them helps you reach **individuals** who share and engage.

<div class="lead">

We curate from these creators in our [daily digest](/). When we feature a piece, it appears on the homepage, in the [RSS feed](/feed.xml), and in **Recent from creators** below. If you publish a tech newsletter or blog and want to be considered, [get in touch](/about/).

**How this page is fed:** Creator *sources* are taken automatically from `const.py`: any source with `type: 'creator'` is listed below. The pipeline reserves a **creator slot** per day and picks the best post from those sources; that post gets `source_type: creator` and appears under "Recent from creators". Add more feeds in `const.py` with `'type': 'creator'` to grow the list and the stream.

</div>

<div class="source-list">

{% if site.data.creator_sources and site.data.creator_sources.size > 0 %}
{% for src in site.data.creator_sources %}
<div class="source-item">
<a href="{{ src.url }}" target="_blank" rel="noopener">{{ src.name }}</a>
<p>Creator source we curate from — posts appear in the digest and below.</p>
<span class="badge">Newsletter</span>
</div>
{% endfor %}
{% else %}
<p class="source-item" style="grid-column:1/-1;">No creator sources in <code>const.py</code> yet. Add entries with <code>type: 'creator'</code> and run the news pipeline to populate this list automatically.</p>
{% endif %}

</div>

{% assign creator_posts = site.posts | where_exp: "p", "p.source_type == 'creator'" %}
{% if creator_posts.size > 0 %}
<div class="recent">
<h2>Recent from creators</h2>
{% for post in creator_posts limit: 10 %}
<div class="post-item">
  {% if post.external_url %}
  <a href="{{ post.external_url }}" target="_blank" rel="noopener">{{ post.title }}</a>
  {% else %}
  <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
  {% endif %}
  <div class="post-meta">{{ post.date | date: "%b %d, %Y" }} · {{ post.source }}</div>
</div>
{% endfor %}
</div>
{% endif %}

<p style="margin-top:2rem; font-size:0.9rem; color:#666;"><a href="/">← Back to digest</a> · <a href="/sources/">All sources</a></p>

</div>
