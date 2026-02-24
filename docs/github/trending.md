---
layout: page
title: "GitHub Hot Repos"
description: "Hot GitHub repositories tracked daily. Stars, forks, languages, and contributors — the hottest open source projects right now."
permalink: /github/
---

## Overview

{% assign repos = site.data.github.repos %}
{% assign top_lang = site.data.github.top_language %}
{% assign most_starred = repos | first %}

<div style="display:flex; gap:1em; flex-wrap:wrap; margin-bottom:1.5em;">
  <span style="padding:4px 12px; border-radius:12px; background:#dbeafe; color:#1e40af; font-weight:bold;">Repos: {{ repos.size }}</span>
  <span style="padding:4px 12px; border-radius:12px; background:#dcfce7; color:#166534; font-weight:bold;">Top Language: {{ top_lang }}</span>
  {% if most_starred %}<span style="padding:4px 12px; border-radius:12px; background:#fef3c7; color:#92400e; font-weight:bold;">Most Starred: {{ most_starred.name }} ({{ most_starred.stars }})</span>{% endif %}
</div>

## Charts

<div style="display:flex; gap:2em; flex-wrap:wrap; margin-bottom:2em;">
  <div style="flex:1; min-width:280px; max-width:400px;">
    <h3 style="font-size:1rem; margin-bottom:0.5rem;">Language Distribution</h3>
    <canvas id="langChart" width="380" height="380"></canvas>
  </div>
  <div style="flex:2; min-width:300px;">
    <h3 style="font-size:1rem; margin-bottom:0.5rem;">Top Repos by Stars</h3>
    <canvas id="starsChart" width="600" height="380"></canvas>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
<script>
new Chart(document.getElementById('langChart'), {
  type: 'doughnut',
  data: {
    labels: ["TypeScript", "Python", "Shell", "JavaScript", "C", "C++", "Dart", "MDX", "Batchfile", "Go"],
    datasets: [{ data: [8, 8, 3, 2, 1, 1, 1, 1, 1, 1], backgroundColor: ["#3178c6", "#3572A5", "#89e051", "#f1e05a", "#555555", "#f34b7d", "#00B4AB", "#9ca3af", "#9ca3af", "#00ADD8"] }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { position: 'bottom', labels: { boxWidth: 12, padding: 8, font: { size: 11 } } }
    }
  }
});
new Chart(document.getElementById('starsChart'), {
  type: 'bar',
  data: {
    labels: ["freeCodeCamp", "free-programming-boo", "developer-roadmap", "awesome-selfhosted", "react", "openclaw", "linux", "tensorflow", "ohmyzsh", "vscode"],
    datasets: [{ label: 'Stars', data: [437473, 382997, 349687, 274854, 243332, 223422, 218502, 193895, 184971, 182028], backgroundColor: '#f59e0b', borderRadius: 4 }]
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    plugins: { legend: { display: false } },
    scales: { x: { ticks: { callback: function(v) { return v >= 1000 ? (v/1000).toFixed(0) + 'k' : v; } } } }
  }
});
</script>

## Trending Repositories

{% for repo in repos %}
<div style="margin-bottom:1.2em; padding:0.75em; border:1px solid #e5e7eb; border-radius:8px;">
  <div style="display:flex; align-items:center; gap:0.5em;">
    <img src="{{ repo.owner_avatar }}&s=24" alt="" width="24" height="24" style="border-radius:50%;" loading="lazy">
    <strong><a href="{{ repo.repo_url }}" target="_blank" rel="noopener">{{ repo.name }}</a></strong>
    {% if repo.language %}
      <span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; background:{% if repo.language == 'Python' %}#3572A5{% elsif repo.language == 'JavaScript' %}#b08800{% elsif repo.language == 'TypeScript' %}#3178c6{% elsif repo.language == 'Rust' %}#dea584{% elsif repo.language == 'Go' %}#00ADD8{% elsif repo.language == 'Java' %}#b07219{% elsif repo.language == 'C++' %}#f34b7d{% elsif repo.language == 'C' %}#555{% elsif repo.language == 'C#' %}#178600{% elsif repo.language == 'Ruby' %}#701516{% elsif repo.language == 'Swift' %}#F05138{% elsif repo.language == 'Kotlin' %}#A97BFF{% else %}#6b7280{% endif %};">{{ repo.language }}</span>
    {% endif %}
    {% if repo.license != 'Unknown' %}
      <span style="font-size:0.75em; color:#6b7280; border:1px solid #e5e7eb; padding:1px 6px; border-radius:8px;">{{ repo.license }}</span>
    {% endif %}
  </div>
  <p style="margin:0.3em 0; font-size:0.9em; color:#374151;">{{ repo.description }}</p>
  <span style="font-size:0.85em; color:#6b7280;">
    &#9733; {{ repo.stars }}
    &middot; &#127860; {{ repo.forks }}
    &middot; Issues: {{ repo.open_issues }}
    &middot; Updated: {{ repo.last_push | date: '%b %d, %Y' }}
  </span>
  <br><span style="font-size:0.8em; color:#9ca3af;">
    Owner: <a href="{{ repo.owner_url }}" target="_blank" rel="noopener" style="color:#6b7280;">{{ repo.owner_login }}</a>
    &middot; Created: {{ repo.created_at | date: '%b %d, %Y' }}
  </span>
  {% if repo.topics.size > 0 %}
  <br><span style="font-size:0.75em;">
    {% for topic in repo.topics %}
      <span style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#f3f4f6; border-radius:6px; color:#374151;">{{ topic }}</span>
    {% endfor %}
  </span>
  {% endif %}
</div>
{% endfor %}

---

<p style="font-size:0.8em; color:#9ca3af;">
Data from <a href="https://github.com">GitHub</a> Search API &middot; Updated: {{ site.data.github.generated_at }}
</p>
