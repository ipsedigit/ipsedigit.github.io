---
layout: default
title: ipsedigit
---

<p class="subtitle">{{ site.description }}</p>
{% for post in site.posts %}
  <article>
    <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
    {{ post.content }}
  </article>
{% endfor %}