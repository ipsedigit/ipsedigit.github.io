---
layout: default
title: ipsedigit
---

<style>
.post-item {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #eee;
}

.post-item:last-child {
  border-bottom: none;
}

.post-meta {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.post-tags {
  display: inline;
}

.post-tags a {
  color: #666;
  text-decoration: none;
  margin-right: 0.5rem;
}

.post-tags a:hover {
  text-decoration: underline;
}

.post-title {
  margin: 0.5rem 0;
  font-size: 1.3rem;
}

.post-title a {
  color: #111;
  text-decoration: none;
}

.post-title a:hover {
  text-decoration: underline;
}

.post-excerpt {
  color: #444;
  line-height: 1.6;
}

.post-excerpt img {
  max-width: 100%;
  margin: 1rem 0;
}

.post-excerpt blockquote {
  border-left: 3px solid #ddd;
  margin: 1rem 0;
  padding-left: 1rem;
  color: #555;
  font-style: italic;
}
</style>

{% for post in site.posts %}
<article class="post-item">
  <div class="post-meta">
    <time>{{ post.date | date: "%d %b %Y" }}</time>
    &middot;
    <span class="post-tags">
      {% for category in post.categories %}
        {% assign tag_slug = category | slugify: "latin" %}
        {% capture tag_url %}/tags/{{ tag_slug }}/{% endcapture %}
        <a href="{{ tag_url }}">{{ category }}</a>{% unless forloop.last %},{% endunless %}
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
{% endfor %}
