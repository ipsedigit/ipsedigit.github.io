---
layout: default
title: ipsedigit
---

<style>
:root {
  --primary: #667eea;
  --primary-dark: #764ba2;
  --text-dark: #1a1a1a;
  --text-muted: #666;
  --bg-light: #f8f9fa;
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.08);
  --shadow-md: 0 4px 16px rgba(0,0,0,0.12);
  --radius: 12px;
}

/* Hero Section */
.hero {
  text-align: center;
  padding: 40px 20px;
  margin-bottom: 30px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  border-radius: var(--radius);
  color: #fff;
}

.hero h1 {
  font-size: 2.5rem;
  margin: 0 0 10px 0;
}

.hero p {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0;
}

/* Navigation */
.site-nav {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.nav-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #fff;
  border-radius: 25px;
  color: var(--text-dark);
  text-decoration: none;
  font-weight: 500;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
}

.nav-link:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
  color: var(--primary);
}

.nav-link.active {
  background: var(--primary);
  color: #fff;
}

/* Posts Container */
.posts-container {
  max-width: 800px;
  margin: 0 auto;
}

/* Post Card */
.post-card {
  background: #fff;
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
  margin-bottom: 24px;
  padding: 24px;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
  overflow: hidden;
}

.post-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-3px);
}

/* Post Meta */
.post-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
  font-size: 0.85rem;
  flex-wrap: wrap;
}

.post-date {
  background: var(--bg-light);
  padding: 5px 12px;
  border-radius: 20px;
  color: var(--text-muted);
  font-weight: 500;
}

/* Tags */
.post-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.post-tag {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: #fff;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
}

.post-tag:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  color: #fff;
}

/* Post Title */
.post-title {
  margin: 0 0 16px 0;
  font-size: 1.5rem;
  line-height: 1.3;
}

.post-title a {
  color: var(--text-dark);
  text-decoration: none;
  transition: color 0.2s ease;
}

.post-title a:hover {
  color: var(--primary);
}

/* Post Content */
.post-content {
  color: #444;
  line-height: 1.7;
}

.post-content img {
  max-width: 100%;
  border-radius: 8px;
  margin: 16px 0;
  box-shadow: var(--shadow-sm);
}

.post-content blockquote {
  border-left: 4px solid var(--primary);
  margin: 16px 0;
  padding: 16px 20px;
  background: var(--bg-light);
  border-radius: 0 8px 8px 0;
  font-style: italic;
  color: #555;
}

.post-content h3 {
  margin-top: 0;
  font-size: 1.1rem;
}

.post-content h3 a {
  color: var(--primary);
  text-decoration: none;
}

.post-content h3 a:hover {
  text-decoration: underline;
}

/* Quote Card */
.quote-card {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: #fff;
  position: relative;
}

.quote-card::before {
  content: '"';
  position: absolute;
  top: 10px;
  right: 20px;
  font-size: 6rem;
  opacity: 0.15;
  font-family: Georgia, serif;
  line-height: 1;
}

.quote-card .post-date {
  background: rgba(255,255,255,0.2);
  color: #fff;
}

.quote-card .post-tag {
  background: rgba(255,255,255,0.25);
  color: #fff;
}

.quote-card .post-tag:hover {
  background: rgba(255,255,255,0.4);
}

.quote-card .post-title a {
  color: #fff;
}

.quote-card .post-content {
  color: rgba(255,255,255,0.95);
  font-size: 1.15rem;
  font-style: italic;
}

/* News Card */
.news-card {
  border-left: 4px solid var(--primary);
}

/* Responsive */
@media (max-width: 600px) {
  .hero {
    padding: 30px 15px;
  }
  .hero h1 {
    font-size: 1.8rem;
  }
  .post-card {
    padding: 18px;
    margin-bottom: 18px;
  }
  .post-title {
    font-size: 1.2rem;
  }
  .post-meta {
    gap: 8px;
  }
  .site-nav {
    gap: 10px;
  }
  .nav-link {
    padding: 8px 16px;
    font-size: 0.9rem;
  }
}
</style>

<div class="posts-container">
  <div class="hero">
    <h1>🚀 ipsedigit</h1>
    <p>The blog you never asked for</p>
  </div>

  <nav class="site-nav">
    <a href="{{ '/' | relative_url }}" class="nav-link active">
      📰 Tutti i Post
    </a>
    <a href="{{ '/tags/' | relative_url }}" class="nav-link">
      🏷️ Tags
    </a>
  </nav>

{% for post in site.posts %}
  {% assign is_quote = false %}
  {% assign is_news = false %}
  {% if post.categories contains 'quotes' %}
    {% assign is_quote = true %}
  {% else %}
    {% assign is_news = true %}
  {% endif %}
  
  <article class="post-card {% if is_quote %}quote-card{% elsif is_news %}news-card{% endif %}">
    <div class="post-meta">
      <span class="post-date">📅 {{ post.date | date: "%d %b %Y" }}</span>
      <div class="post-tags">
        {% for category in post.categories %}
          <a href="{{ '/tags/' | relative_url }}#{{ category | slugify }}" class="post-tag">{{ category }}</a>
        {% endfor %}
      </div>
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
