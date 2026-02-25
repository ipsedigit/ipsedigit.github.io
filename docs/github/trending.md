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

## 🏆 Repo of the Day

<div style="margin-bottom:1.5em; padding:1em; border:2px solid #f59e0b; border-radius:12px; background:#fffbeb;">
  <div style="display:flex; align-items:center; gap:0.5em; margin-bottom:0.5em; flex-wrap:wrap;">
    <img src="https://avatars.githubusercontent.com/u/9892522?v=4&s=32" alt="" width="32" height="32" style="border-radius:50%;">
    <strong style="font-size:1.2em;"><a href="https://github.com/freeCodeCamp/freeCodeCamp" target="_blank" rel="noopener">freeCodeCamp/freeCodeCamp</a></strong>
    <span style="padding:2px 8px; border-radius:12px; font-size:0.8em; background:#fbbf24; color:#78350f;">⭐ Repo of the Day</span>
    <span style="font-size:0.85em; color:#92400e;">0 stars today</span>
  </div>
  <p style="margin:0.3em 0; color:#374151;">freeCodeCamp.org's open-source codebase and curriculum. Learn math, programming, and computer science for free.</p>
  <div style="display:flex; gap:1em; font-size:0.85em; color:#6b7280; flex-wrap:wrap;">
    <span>&#9733; 437,513</span>
    <span>&#127860; 43,442</span>
    <span>TypeScript</span>
    <span>BSD-3-Clause</span>
  </div>
  <div style="margin-top:0.5em;"><span style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#fef3c7; border-radius:6px; color:#92400e; font-size:0.75em;">careers</span> <span style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#fef3c7; border-radius:6px; color:#92400e; font-size:0.75em;">certification</span> <span style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#fef3c7; border-radius:6px; color:#92400e; font-size:0.75em;">community</span> <span style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#fef3c7; border-radius:6px; color:#92400e; font-size:0.75em;">curriculum</span> <span style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#fef3c7; border-radius:6px; color:#92400e; font-size:0.75em;">d3</span> <span style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#fef3c7; border-radius:6px; color:#92400e; font-size:0.75em;">education</span> <span style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#fef3c7; border-radius:6px; color:#92400e; font-size:0.75em;">freecodecamp</span> <span style="display:inline-block; padding:1px 6px; margin:2px 2px 0 0; background:#fef3c7; border-radius:6px; color:#92400e; font-size:0.75em;">javascript</span></div>
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
  <div style="flex:2; min-width:300px;">
    <h3 style="font-size:1rem; margin-bottom:0.5rem;">Top Movers (24h)</h3>
    <canvas id="moversChart" width="600" height="380"></canvas>
  </div>
</div>

<div style="display:flex; gap:2em; flex-wrap:wrap; margin-bottom:2em;">
  <div style="flex:1; min-width:300px;">
    <h3 style="font-size:1rem; margin-bottom:0.5rem;">New Entries Per Day</h3>
    <canvas id="newEntriesChart" width="500" height="300"></canvas>
  </div>
  <div style="flex:1; min-width:300px;">
    <h3 style="font-size:1rem; margin-bottom:0.5rem;">Language Trends (14d)</h3>
    <canvas id="langTrendChart" width="500" height="300"></canvas>
  </div>
</div>

<div style="display:flex; gap:2em; flex-wrap:wrap; margin-bottom:2em;">
  <div style="flex:1; min-width:300px; max-width:400px;">
    <h3 style="font-size:1rem; margin-bottom:0.5rem;">Push Activity by Day</h3>
    <canvas id="activityChart" width="400" height="300"></canvas>
  </div>
  <div style="flex:2; min-width:300px;">
    <h3 style="font-size:1rem; margin-bottom:0.5rem;">Top Topics</h3>
    <div style="display:flex; flex-wrap:wrap; gap:6px; align-items:baseline;">
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,1.00); border-radius:8px; font-size:2.00em; color:#1e3a5f;">ai <sup style="font-size:0.6em;">5</sup></span>
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,1.00); border-radius:8px; font-size:2.00em; color:#1e3a5f;">claude <sup style="font-size:0.6em;">5</sup></span>
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.90); border-radius:8px; font-size:1.74em; color:#1e3a5f;">javascript <sup style="font-size:0.6em;">4</sup></span>
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.90); border-radius:8px; font-size:1.74em; color:#1e3a5f;">ai-agents <sup style="font-size:0.6em;">4</sup></span>
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.90); border-radius:8px; font-size:1.74em; color:#1e3a5f;">claude-code <sup style="font-size:0.6em;">4</sup></span>
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.80); border-radius:8px; font-size:1.48em; color:#1e3a5f;">python <sup style="font-size:0.6em;">3</sup></span>
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.80); border-radius:8px; font-size:1.48em; color:#1e3a5f;">anthropic <sup style="font-size:0.6em;">3</sup></span>
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.70); border-radius:8px; font-size:1.22em; color:#1e3a5f;">curriculum <sup style="font-size:0.6em;">2</sup></span>
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.70); border-radius:8px; font-size:1.22em; color:#1e3a5f;">education <sup style="font-size:0.6em;">2</sup></span>
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.70); border-radius:8px; font-size:1.22em; color:#1e3a5f;">hacktoberfest <sup style="font-size:0.6em;">2</sup></span>
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.70); border-radius:8px; font-size:1.22em; color:#1e3a5f;">computer-science <sup style="font-size:0.6em;">2</sup></span>
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.70); border-radius:8px; font-size:1.22em; color:#1e3a5f;">deep-learning <sup style="font-size:0.6em;">2</sup></span>
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.70); border-radius:8px; font-size:1.22em; color:#1e3a5f;">machine-learning <sup style="font-size:0.6em;">2</sup></span>
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.70); border-radius:8px; font-size:1.22em; color:#1e3a5f;">cli <sup style="font-size:0.6em;">2</sup></span>
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.70); border-radius:8px; font-size:1.22em; color:#1e3a5f;">artificial-intelligence <sup style="font-size:0.6em;">2</sup></span>
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.70); border-radius:8px; font-size:1.22em; color:#1e3a5f;">automation <sup style="font-size:0.6em;">2</sup></span>
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.70); border-radius:8px; font-size:1.22em; color:#1e3a5f;">deepseek <sup style="font-size:0.6em;">2</sup></span>
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.70); border-radius:8px; font-size:1.22em; color:#1e3a5f;">gemma <sup style="font-size:0.6em;">2</sup></span>
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.70); border-radius:8px; font-size:1.22em; color:#1e3a5f;">glm <sup style="font-size:0.6em;">2</sup></span>
      <span style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.70); border-radius:8px; font-size:1.22em; color:#1e3a5f;">llm <sup style="font-size:0.6em;">2</sup></span>
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
<script>
new Chart(document.getElementById('langChart'), {
  type: 'doughnut',
  data: {
    labels: ["TypeScript", "Python", "JavaScript", "Shell", "C", "HTML", "C++", "Jupyter Notebook", "Dart", "MDX"],
    datasets: [{ data: [8, 8, 3, 3, 1, 1, 1, 1, 1, 1], backgroundColor: ["#3178c6", "#3572A5", "#f1e05a", "#89e051", "#555555", "#e34c26", "#f34b7d", "#DA5B0B", "#00B4AB", "#9ca3af"] }]
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
    labels: ["freeCodeCamp", "free-programming-boo", "developer-roadmap", "awesome-python", "react", "openclaw", "linux", "computer-science", "tensorflow", "ohmyzsh"],
    datasets: [{ label: 'Stars', data: [437513, 383034, 349734, 284497, 243351, 227246, 218660, 201703, 193905, 184993], backgroundColor: '#f59e0b', borderRadius: 4 }]
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    plugins: { legend: { display: false } },
    scales: { x: { ticks: { callback: function(v) { return v >= 1000 ? (v/1000).toFixed(0) + 'k' : v; } } } }
  }
});
new Chart(document.getElementById('moversChart'), {
  type: 'bar',
  data: {
    labels: [],
    datasets: [{ label: 'Star Change', data: [], backgroundColor: [], borderRadius: 4 }]
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    plugins: { legend: { display: false } },
    scales: { x: { ticks: { callback: function(v) { return (v > 0 ? '+' : '') + v; } } } }
  }
});
// New Entries Per Day
new Chart(document.getElementById('newEntriesChart'), {
  type: 'bar',
  data: {
    labels: ["02-25"],
    datasets: [{ label: 'New Repos', data: [0], backgroundColor: '#8b5cf6', borderRadius: 4 }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
  }
});
// Language Trends
new Chart(document.getElementById('langTrendChart'), {
  type: 'line',
  data: {
    labels: ["02-25"],
    datasets: [{"label": "TypeScript", "data": [8], "borderColor": "#3572A5", "backgroundColor": "#3572A533", "fill": true, "tension": 0.3}, {"label": "Python", "data": [8], "borderColor": "#f1e05a", "backgroundColor": "#f1e05a33", "fill": true, "tension": 0.3}, {"label": "JavaScript", "data": [3], "borderColor": "#3178c6", "backgroundColor": "#3178c633", "fill": true, "tension": 0.3}, {"label": "Shell", "data": [3], "borderColor": "#dea584", "backgroundColor": "#dea58433", "fill": true, "tension": 0.3}, {"label": "C", "data": [1], "borderColor": "#00ADD8", "backgroundColor": "#00ADD833", "fill": true, "tension": 0.3}]
  },
  options: {
    responsive: true,
    plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, padding: 8, font: { size: 11 } } } },
    scales: { y: { beginAtZero: true, stacked: true, ticks: { stepSize: 1 } }, x: { ticks: { font: { size: 10 } } } }
  }
});
// Push Activity by Day of Week
new Chart(document.getElementById('activityChart'), {
  type: 'bar',
  data: {
    labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    datasets: [{ label: 'Pushes', data: [4, 4, 18, 2, 1, 1, 0], backgroundColor: ["rgba(59, 130, 246, 0.2222222222222222)", "rgba(59, 130, 246, 0.2222222222222222)", "rgba(59, 130, 246, 1.0)", "rgba(59, 130, 246, 0.2)", "rgba(59, 130, 246, 0.2)", "rgba(59, 130, 246, 0.2)", "rgba(59, 130, 246, 0.2)"], borderRadius: 4 }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
  }
});
</script>

## Trending Repositories

{% for repo in repos %}
<div style="margin-bottom:1.2em; padding:0.75em; border:1px solid #e5e7eb; border-radius:8px;">
  <div style="display:flex; align-items:center; gap:0.5em; flex-wrap:wrap;">
    <img src="{{ repo.owner_avatar }}&s=24" alt="" width="24" height="24" style="border-radius:50%;" loading="lazy">
    <strong><a href="{{ repo.repo_url }}" target="_blank" rel="noopener">{{ repo.name }}</a></strong>
    {% if repo.language %}
      <span style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.75em; color:#fff; background:{% if repo.language == 'Python' %}#3572A5{% elsif repo.language == 'JavaScript' %}#b08800{% elsif repo.language == 'TypeScript' %}#3178c6{% elsif repo.language == 'Rust' %}#dea584{% elsif repo.language == 'Go' %}#00ADD8{% elsif repo.language == 'Java' %}#b07219{% elsif repo.language == 'C++' %}#f34b7d{% elsif repo.language == 'C' %}#555{% elsif repo.language == 'C#' %}#178600{% elsif repo.language == 'Ruby' %}#701516{% elsif repo.language == 'Swift' %}#F05138{% elsif repo.language == 'Kotlin' %}#A97BFF{% else %}#6b7280{% endif %};">{{ repo.language }}</span>
    {% endif %}
    {% if repo.license != 'Unknown' %}
      <span style="font-size:0.75em; color:#6b7280; border:1px solid #e5e7eb; padding:1px 6px; border-radius:8px;">{{ repo.license }}</span>
    {% endif %}
    {% if repo.badge == "new_entry" %}
      <span style="padding:2px 8px; border-radius:12px; font-size:0.75em; background:#dbeafe; color:#1e40af; font-weight:bold;">🆕 NEW</span>
    {% elsif repo.badge == "rising" %}
      <span style="padding:2px 8px; border-radius:12px; font-size:0.75em; background:#dcfce7; color:#166534; font-weight:bold;">📈 +{{ repo.star_delta }}</span>
    {% elsif repo.badge == "cooling" %}
      <span style="padding:2px 8px; border-radius:12px; font-size:0.75em; background:#fee2e2; color:#991b1b; font-weight:bold;">📉 {{ repo.star_delta }}</span>
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
