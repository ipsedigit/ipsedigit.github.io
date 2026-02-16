---
layout: default
title: ipsedigit
---

<style>
.posts-container {
  max-width: 800px;
  margin: 0 auto;
}

.post-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  margin-bottom: 24px;
  padding: 24px;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.post-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  transform: translateY(-2px);
}

.post-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  font-size: 0.85rem;
  color: #666;
}

.post-date {
  background: #f0f0f0;
  padding: 4px 10px;
  border-radius: 20px;
}

.post-category {
  background: #e8f4f8;
  color: #0077b6;
  padding: 4px 10px;
  border-radius: 20px;
  font-weight: 500;
}

.post-title {
  margin: 0 0 16px 0;
  font-size: 1.4rem;
  line-height: 1.3;
}

.post-title a {
  color: #1a1a1a;
  text-decoration: none;
}

.post-title a:hover {
  color: #0077b6;
}

.post-content {
  color: #444;
  line-height: 1.6;
}

.post-content img {
  max-width: 100%;
  border-radius: 8px;
  margin: 12px 0;
}

.post-content blockquote {
  border-left: 4px solid #0077b6;
  margin: 16px 0;
  padding: 12px 20px;
  background: #f9f9f9;
  border-radius: 0 8px 8px 0;
  font-style: italic;
  color: #555;
}

.post-content h3 {
  margin-top: 0;
}

.quote-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.quote-card .post-meta .post-date,
.quote-card .post-meta .post-category {
  background: rgba(255,255,255,0.2);
  color: #fff;
}

.quote-card .post-title a {
  color: #fff;
}

.quote-card .post-content {
  color: rgba(255,255,255,0.95);
  font-size: 1.1rem;
  font-style: italic;
}

@media (max-width: 600px) {
  .post-card {
    padding: 16px;
    margin-bottom: 16px;
  }
  .post-title {
    font-size: 1.2rem;
  }
}
</style>

<div class="posts-container">
{% assign sorted_posts = site.posts | sort: 'date' | reverse %}
{% for post in sorted_posts %}
  {% assign is_quote = false %}
  {% if post.categories contains 'quotes' %}
    {% assign is_quote = true %}
  {% endif %}
  
  <article class="post-card {% if is_quote %}quote-card{% endif %}">
    <div class="post-meta">
      <span class="post-date">{{ post.date | date: "%d %b %Y" }}</span>
      {% for category in post.categories %}
        <span class="post-category">{{ category }}</span>
      {% endfor %}
    </div>
    <h2 class="post-title">
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </h2>
    <div class="post-content">
      {{ post.content }}
    </div>
  </article>
{% endfor %}
</div>
