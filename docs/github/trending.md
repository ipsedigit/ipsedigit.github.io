---
layout: page
title: "GitHub Hot Repos"
description: "Hot GitHub repositories tracked daily. Stars, forks, languages, and contributors — the hottest open source projects right now."
permalink: /github/
title_badge: "⭐ GitHub"
title_badge_bg: "#fef3c7"
title_badge_color: "#92400e"
---

{% assign repos = site.data.github.repos %}
{% assign top_lang = site.data.github.top_language %}
{% assign most_starred = repos | first %}

<div style="margin-bottom:1.5em; padding:1em; border:2px solid #f59e0b; border-radius:12px; background:#fffbeb;">
  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap; margin-bottom:0.6em;">
    <span style="padding:3px 10px; border-radius:12px; font-size:0.78em; font-weight:bold; background:#f59e0b; color:#fff;">&#9733; Latest</span>
    <span style="font-size:0.78em; color:#6b7280;">+1103 stars today</span>
  </div>
  <div style="display:flex; align-items:center; gap:0.5em; margin-bottom:0.5em; flex-wrap:wrap;">
    <img src="https://avatars.githubusercontent.com/u/76263028?v=4&s=32" alt="" width="32" height="32" style="border-radius:50%;">
    <strong style="font-size:1.2em;"><a href="https://github.com/anthropics/skills" target="_blank" rel="noopener">anthropics/skills</a></strong>
  </div>
  <p style="margin:0.3em 0; color:#374151;">Public repository for Agent Skills</p>
  <div style="display:flex; gap:1em; font-size:0.85em; color:#6b7280; flex-wrap:wrap;">
    <span>&#9733; 79,062</span>
    <span>&#127860; 8,250</span>
    <span>Python</span>
    <span>Unknown</span>
  </div>
  <div style="margin-top:0.5em;"><a href="/tags/agent-skills/" style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#fef3c7; border-radius:6px; color:#92400e; font-size:0.75em; text-decoration:none;">agent-skills</a></div>
</div>

## Trending Repositories

{% for repo in repos %}
<div style="margin-bottom:1.2em; padding:0.75em; border:1px solid #e5e7eb; border-radius:8px;">
  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap;">
    <img src="{{ repo.owner_avatar }}&s=24" alt="" width="24" height="24" style="border-radius:50%;" loading="lazy">
    <strong><a href="{{ repo.repo_url }}" target="_blank" rel="noopener">{{ repo.name }}</a></strong>
    {% if repo.language %}
      {% assign lang_slug = repo.language | slugify %}
      <a href="/tags/{{ lang_slug }}/" style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; text-decoration:none; background:{% if repo.language == 'Python' %}#3572A5{% elsif repo.language == 'JavaScript' %}#b08800{% elsif repo.language == 'TypeScript' %}#3178c6{% elsif repo.language == 'Rust' %}#dea584{% elsif repo.language == 'Go' %}#00ADD8{% elsif repo.language == 'Java' %}#b07219{% elsif repo.language == 'C++' %}#f34b7d{% elsif repo.language == 'C' %}#555{% elsif repo.language == 'C#' %}#178600{% elsif repo.language == 'Ruby' %}#701516{% elsif repo.language == 'Swift' %}#F05138{% elsif repo.language == 'Kotlin' %}#A97BFF{% else %}#6b7280{% endif %};">{{ repo.language }}</a>
    {% endif %}
    {% if repo.license != 'Unknown' %}
      <a href="{{ repo.repo_url }}" target="_blank" rel="noopener" style="font-size:0.75em; color:#6b7280; border:1px solid #e5e7eb; padding:1px 6px; border-radius:8px; text-decoration:none;">{{ repo.license }}</a>
    {% endif %}
    {% if repo.badge == "new_entry" %}
      <a href="{{ repo.repo_url }}" target="_blank" rel="noopener" style="padding:2px 8px; border-radius:12px; font-size:0.75em; text-decoration:none; background:#dbeafe; color:#1e40af; font-weight:bold;">🆕 NEW</a>
    {% elsif repo.badge == "rising" %}
      <a href="{{ repo.repo_url }}" target="_blank" rel="noopener" style="padding:2px 8px; border-radius:12px; font-size:0.75em; text-decoration:none; background:#dcfce7; color:#166534; font-weight:bold;">📈 +{{ repo.star_delta }}</a>
    {% elsif repo.badge == "cooling" %}
      <a href="{{ repo.repo_url }}" target="_blank" rel="noopener" style="padding:2px 8px; border-radius:12px; font-size:0.75em; text-decoration:none; background:#fee2e2; color:#991b1b; font-weight:bold;">📉 {{ repo.star_delta }}</a>
    {% endif %}
  </div>
  <p style="margin:0.3em 0; font-size:0.9em; color:#374151;">{{ repo.description }}</p>
  <span style="font-size:0.85em; color:#6b7280;">
    &#9733; {{ repo.stars }}
    &middot; &#127860; {{ repo.forks }}
    &middot; Issues: {{ repo.open_issues }}
    &middot; Updated: {{ repo.last_push | date: '%b %d, %Y' }}
    {% if repo.star_delta != 0 %}
      &middot; <span style="color:{% if repo.star_delta > 0 %}#16a34a{% else %}#dc2626{% endif %};">
        {% if repo.star_delta > 0 %}+{% endif %}{{ repo.star_delta }} today
      </span>
    {% endif %}
  </span>
  <br><span style="font-size:0.8em; color:#9ca3af;">
    Owner: <a href="{{ repo.owner_url }}" target="_blank" rel="noopener" style="color:#6b7280;">{{ repo.owner_login }}</a>
    &middot; Created: {{ repo.created_at | date: '%b %d, %Y' }}
  </span>
  {% if repo.topics.size > 0 %}
  <br><span style="font-size:0.75em;">
    {% for topic in repo.topics %}
      {% assign topic_slug = topic | slugify %}<a href="/tags/{{ topic_slug }}/" style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#f3f4f6; border-radius:6px; color:#374151; text-decoration:none;">{{ topic }}</a>
    {% endfor %}
  </span>
  {% endif %}
</div>
{% endfor %}

---

<p style="font-size:0.8em; color:#9ca3af;">Data from <a href="https://github.com">GitHub</a> Search API &middot; Updated: {{ site.data.github.generated_at }}</p>
