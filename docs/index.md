---
layout: home
title: ipsedigit
---
<div class="logo-container" style="text-align: center;">
  <img src="{{ '/assets/images/logo.png' | relative_url }}" alt="ipsedigit logo" style="max-width: 200px; margin-bottom: 20px;">
</div>
{% for post in site.posts %}
  <article>
    <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
    {{ post.content }}
  </article>
{% endfor %}