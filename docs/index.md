---
layout: default
---

<h1>ipsedigit</h1>

{% for post in site.posts %}
  <article>
    <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
    {{ post.content }}
  </article>
{% endfor %}