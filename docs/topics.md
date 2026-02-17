---
layout: default
title: Browse Topics | Argomenti | Sujets | Temas - eof.news
description: "Browse tech articles by topic: AI, Programming, Security, Startups. Sfoglia per argomento. Parcourir par sujet. Explorar por tema."
permalink: /topics/
---

<style>
.topics-page h1 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  font-family: 'JetBrains Mono', monospace;
}
.topics-page > p {
  color: #666;
  margin-bottom: 2rem;
  font-size: 0.9rem;
}
.topic-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}
.topic-card {
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 1.25rem;
  background: #fafafa;
  transition: all 0.2s;
}
.topic-card:hover {
  border-color: #999;
  background: #fff;
}
.topic-card h2 {
  font-size: 1.1rem;
  margin: 0 0 0.5rem 0;
}
.topic-card h2 a {
  color: #111;
  text-decoration: none;
}
.topic-card h2 a:hover {
  color: #0066cc;
}
.topic-card p {
  color: #666;
  font-size: 0.85rem;
  margin: 0 0 0.75rem 0;
  line-height: 1.5;
}
.topic-card .count {
  font-size: 0.8rem;
  color: #888;
}
</style>

<div class="topics-page">

# Browse by Topic

Explore articles organized by category

<div class="topic-grid">

{% assign all_categories = "" | split: "" %}
{% for post in site.posts %}
  {% for cat in post.categories %}
    {% unless all_categories contains cat %}
      {% assign all_categories = all_categories | push: cat %}
    {% endunless %}
  {% endfor %}
{% endfor %}

{% for category in all_categories %}
{% assign cat_slug = category | slugify: "latin" %}
{% assign cat_posts = site.posts | where_exp: "post", "post.categories contains category" %}
<div class="topic-card">
  <h2><a href="/tags/{{ cat_slug }}/">{{ category }}</a></h2>
  <p class="count">{{ cat_posts.size }} articles</p>
</div>
{% endfor %}

</div>

</div>

