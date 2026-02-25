---
layout: page
title: "Trend Dashboard"
description: "Rising and falling tech topics, most active sources, and top stories this week on eof.news"
permalink: /trends/
---

{% include freshness-banner.html timestamp=site.data.trends.generated_at %}

## Rising Topics

{% if site.data.trends.rising_topics.size > 0 %}
<div class="trends-list">
{% for topic in site.data.trends.rising_topics %}
<div class="trend-item trend-rising">
  <span class="trend-arrow" style="color: #22c55e;">&#9650;</span>
  <span class="trend-topic"><strong>{{ topic.topic }}</strong></span>
  <span class="trend-count">{{ topic.count_this_week }} posts</span>
  <span class="trend-change" style="color: #22c55e;">+{{ topic.change }}</span>
  <span class="trend-bar" style="display:inline-block; background:#22c55e; height:8px; width:{{ topic.count_this_week | times: 8 }}px; border-radius:4px;"></span>
</div>
{% endfor %}
</div>
{% else %}
<p>No rising topics this week.</p>
{% endif %}

## Falling Topics

{% if site.data.trends.falling_topics.size > 0 %}
<div class="trends-list">
{% for topic in site.data.trends.falling_topics %}
<div class="trend-item trend-falling">
  <span class="trend-arrow" style="color: #ef4444;">&#9660;</span>
  <span class="trend-topic"><strong>{{ topic.topic }}</strong></span>
  <span class="trend-count">{{ topic.count_this_week }} posts</span>
  <span class="trend-change" style="color: #ef4444;">{{ topic.change }}</span>
</div>
{% endfor %}
</div>
{% else %}
<p>No falling topics this week.</p>
{% endif %}

## Most Active Sources

{% if site.data.trends.active_sources.size > 0 %}
| Source | Posts This Week |
|--------|----------------|
{% for src in site.data.trends.active_sources %}
| {{ src.source }} | {{ src.count }} |
{% endfor %}
{% else %}
<p>No source data available.</p>
{% endif %}

## Top Stories This Week

{% if site.data.trends.top_stories.size > 0 %}
{% for story in site.data.trends.top_stories %}
<div class="top-story" style="margin-bottom: 1em; padding: 0.5em 0; border-bottom: 1px solid #e5e7eb;">
  <strong><a href="{{ story.external_url }}">{{ story.title }}</a></strong>
  <br>
  <span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.8em; background:#dbeafe; color:#1e40af;">score: {{ story.score }}</span>
  <span style="font-size:0.85em; color:#6b7280;">{{ story.source }} &middot; {{ story.date }}</span>
</div>
{% endfor %}
{% else %}
<p>No stories this week.</p>
{% endif %}

---

<p style="font-size:0.8em; color:#9ca3af;">
{{ site.data.trends.total_posts_this_week }} posts this week vs {{ site.data.trends.total_posts_prev_week }} last week
</p>
