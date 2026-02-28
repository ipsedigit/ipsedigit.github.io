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
{% assign featured = repos | where: "name", site.data.github.repo_of_the_day | first %}
{% unless featured %}{% assign featured = repos | first %}{% endunless %}

{% if featured %}
<div style="margin-bottom:2em; padding:1.25em; border:2px solid #f59e0b; border-radius:8px; background:#fffbeb;">
  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap; margin-bottom:0.6em;">
    <span style="padding:3px 10px; border-radius:12px; font-size:0.78em; font-weight:bold; background:#f59e0b; color:#fff;">&#9733; Repo of the Day</span>
    <span style="font-size:0.78em; color:#6b7280;">{{ featured.owner_login }}{% if featured.language %} &middot; {{ featured.language }}{% endif %}</span>
  </div>
  <div style="font-weight:700; font-size:1.1em; margin-bottom:0.4em;">
    <a href="{{ featured.repo_url }}" target="_blank" rel="noopener" style="color:#92400e; text-decoration:none;">{{ featured.name }}</a>
    {% if featured.badge == "new_entry" %}<span style="padding:2px 8px; border-radius:12px; font-size:0.75em; background:#dbeafe; color:#1e40af; font-weight:bold; margin-left:0.4em;">🆕 NEW</span>{% elsif featured.badge == "rising" %}<span style="padding:2px 8px; border-radius:12px; font-size:0.75em; background:#dcfce7; color:#166534; font-weight:bold; margin-left:0.4em;">📈 +{{ featured.star_delta }}</span>{% endif %}
  </div>
  <p style="margin:0 0 0.4em 0; font-size:0.88em; color:#374151; line-height:1.5;">{{ featured.description }}</p>
  <span style="font-size:0.78em; color:#9ca3af;">&#9733; {{ featured.stars }} &middot; &#127860; {{ featured.forks }} &middot; Issues: {{ featured.open_issues }}</span>
  {% if featured.topics.size > 0 %}
  <div style="margin-top:0.5em; display:flex; gap:0.3em; flex-wrap:wrap;">
    {% for topic in featured.topics limit:5 %}
      {% assign topic_slug = topic | slugify %}<a href="/tags/{{ topic_slug }}/" style="padding:2px 6px; background:#fef3c7; border-radius:4px; font-size:0.75em; color:#92400e; text-decoration:none;">{{ topic }}</a>
    {% endfor %}
  </div>
  {% endif %}
</div>
{% endif %}

{% for repo in repos %}
<div style="margin-bottom:1.25em; padding:0.85em; border:1px solid #e5e7eb; border-left:3px solid #fcd34d; border-radius:8px;">
  <div style="margin-bottom:0.3em;">
    <strong><a href="{{ repo.repo_url }}" target="_blank" rel="noopener">{{ repo.name }}</a></strong>
    {% if repo.language %}
      {% assign lang_slug = repo.language | slugify %}
      <a href="/tags/{{ lang_slug }}/" style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; text-decoration:none; margin-left:0.4em; background:{% if repo.language == 'Python' %}#3572A5{% elsif repo.language == 'JavaScript' %}#b08800{% elsif repo.language == 'TypeScript' %}#3178c6{% elsif repo.language == 'Rust' %}#dea584{% elsif repo.language == 'Go' %}#00ADD8{% elsif repo.language == 'Java' %}#b07219{% elsif repo.language == 'C++' %}#f34b7d{% elsif repo.language == 'C' %}#555{% elsif repo.language == 'C#' %}#178600{% elsif repo.language == 'Ruby' %}#701516{% elsif repo.language == 'Swift' %}#F05138{% elsif repo.language == 'Kotlin' %}#A97BFF{% else %}#6b7280{% endif %};">{{ repo.language }}</a>
    {% endif %}
    {% if repo.badge == "new_entry" %}
      <span style="padding:2px 8px; border-radius:12px; font-size:0.75em; background:#dbeafe; color:#1e40af; font-weight:bold; margin-left:0.4em;">🆕 NEW</span>
    {% elsif repo.badge == "rising" %}
      <span style="padding:2px 8px; border-radius:12px; font-size:0.75em; background:#dcfce7; color:#166534; font-weight:bold; margin-left:0.4em;">📈 +{{ repo.star_delta }}</span>
    {% elsif repo.badge == "cooling" %}
      <span style="padding:2px 8px; border-radius:12px; font-size:0.75em; background:#fee2e2; color:#991b1b; font-weight:bold; margin-left:0.4em;">📉 {{ repo.star_delta }}</span>
    {% endif %}
  </div>
  <p style="margin:0 0 0.4em 0; font-size:0.88em; color:#374151; line-height:1.5;">{{ repo.description }}</p>
  <span style="font-size:0.78em; color:#9ca3af;">
    &#9733; {{ repo.stars }} &middot; &#127860; {{ repo.forks }} &middot; {{ repo.owner_login }} &middot; {{ repo.last_push | date: '%b %d, %Y' }}{% if repo.star_delta != 0 %} &middot; <span style="color:{% if repo.star_delta > 0 %}#16a34a{% else %}#dc2626{% endif %};">{% if repo.star_delta > 0 %}+{% endif %}{{ repo.star_delta }} today</span>{% endif %}
  </span>
  {% if repo.topics.size > 0 %}
  <div style="margin-top:0.4em; display:flex; gap:0.3em; flex-wrap:wrap;">
    {% for topic in repo.topics %}
      {% assign topic_slug = topic | slugify %}<a href="/tags/{{ topic_slug }}/" style="padding:1px 6px; background:#f3f4f6; border-radius:4px; font-size:0.75em; color:#374151; text-decoration:none;">{{ topic }}</a>
    {% endfor %}
  </div>
  {% endif %}
</div>
{% endfor %}

---

<p style="font-size:0.8em; color:#9ca3af;">Data from <a href="https://github.com">GitHub</a> Search API &middot; Updated: {{ site.data.github.generated_at }}</p>
