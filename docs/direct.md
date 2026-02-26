---
layout: base
title: Direct | eof.news
description: "Recent articles from developers we follow. Same as the rest of the site: links to articles, not sites."
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
.direct-page .post-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.direct-page .post-list li {
  padding: 0.6rem 0;
  border-bottom: 1px solid #eee;
}
.direct-page .post-list li:last-child {
  border-bottom: none;
}
.direct-page .post-list .date {
  font-size: 0.8rem;
  color: #888;
  margin-right: 0.75rem;
}
.direct-page .post-list a {
  color: #111;
  text-decoration: none;
  font-weight: 500;
}
.direct-page .post-list a:hover {
  color: #0066cc;
}
.direct-page .post-list .source {
  font-size: 0.8rem;
  color: #666;
  margin-left: 0.5rem;
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
}
.direct-page .source-item a {
  color: #111;
  text-decoration: none;
  font-weight: 500;
}
.direct-page .source-item a:hover {
  color: #0066cc;
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
</style>

<div class="direct-page">

# Direct

<p>Recent articles from developers and newsletters we follow. Links go to the <strong>article</strong>, like on Home and the rest of the site — not to a list of sites.</p>

<div class="source-category">
<h2>Recent articles</h2>
<p class="sub">From our curated feeds (DIRECT_FEEDS in const.py). Run <code>python main.py --action direct</code> to refresh.</p>
<ul class="post-list">
{% if site.data.direct_articles and site.data.direct_articles.articles and site.data.direct_articles.articles.size > 0 %}
{% for art in site.data.direct_articles.articles %}
<li>
  <span class="date">{{ art.date }}</span>
  <a href="{{ art.url }}" target="_blank" rel="noopener">{{ art.title | escape }}</a>
  <span class="source">{{ art.source }}</span>
</li>
{% endfor %}
{% else %}
<li>No articles yet. Run <code>python main.py --action direct</code> to fetch from DIRECT_FEEDS.</li>
{% endif %}
</ul>
</div>

<div class="source-category">
<h2>Who links to us</h2>
<p class="sub">Sites that link back to eof.news. If you link to us, <a href="/about/">tell us</a> and we'll add you here.</p>
<div class="source-list">
{% if site.data.links_back.links and site.data.links_back.links.size > 0 %}
{% for item in site.data.links_back.links %}
<div class="source-item">
<a href="{{ item.url }}" target="_blank" rel="noopener">{{ item.name }}</a>
</div>
{% endfor %}
{% else %}
<p>No one listed yet. When we discover or you tell us you link to eof.news, we add you here.</p>
{% endif %}
</div>
</div>

<p class="footer-links"><a href="/">Home</a> · <a href="/sources/">Sources</a> · <a href="/about/">Get in touch</a></p>

</div>
