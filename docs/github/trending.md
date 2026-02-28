---
layout: page
title: "GitHub Hot Repos"
description: "Hot GitHub repositories tracked daily. Stars, forks, languages, and contributors — the hottest open source projects right now."
permalink: /github/
---

{% assign repos = site.data.github.repos %}
{% assign top_lang = site.data.github.top_language %}
{% assign most_starred = repos | first %}

<div style="display:flex; gap:1em; flex-wrap:wrap; margin-bottom:1.5em;">
  <span style="padding:4px 12px; border-radius:12px; background:#fef3c7; color:#92400e; font-weight:bold;">&#11088; GitHub</span>
  <span style="padding:4px 12px; border-radius:12px; background:#f3f4f6; color:#374151; font-weight:bold;">{{ repos.size }} repos</span>
  {% if top_lang %}<span style="padding:4px 12px; border-radius:12px; background:#f3f4f6; color:#374151; font-weight:bold;">{{ top_lang }}</span>{% endif %}
</div>

## 🏆 Repo of the Day

<div style="margin-bottom:1.5em; padding:1em; border:2px solid #f59e0b; border-radius:12px; background:#fffbeb;">
  <div style="display:flex; align-items:center; gap:0.5em; margin-bottom:0.5em; flex-wrap:wrap;">
    <img src="https://avatars.githubusercontent.com/u/76263028?v=4&s=32" alt="" width="32" height="32" style="border-radius:50%;">
    <strong style="font-size:1.2em;"><a href="https://github.com/anthropics/skills" target="_blank" rel="noopener">anthropics/skills</a></strong>
    <a href="https://github.com/anthropics/skills" target="_blank" rel="noopener" style="padding:2px 8px; border-radius:12px; font-size:0.8em; background:#fbbf24; color:#78350f; text-decoration:none;">⭐ Repo of the Day</a>
    <span style="font-size:0.85em; color:#92400e;">+1103 stars today</span>
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
      <a href="/tags/ai/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,1.00); border-radius:8px; font-size:2.00em; color:#1e3a5f; text-decoration:none;">ai <sup style="font-size:0.6em;">6</sup></a>
      <a href="/tags/claude/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.92); border-radius:8px; font-size:1.78em; color:#1e3a5f; text-decoration:none;">claude <sup style="font-size:0.6em;">5</sup></a>
      <a href="/tags/claude-code/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.83); border-radius:8px; font-size:1.57em; color:#1e3a5f; text-decoration:none;">claude-code <sup style="font-size:0.6em;">4</sup></a>
      <a href="/tags/javascript/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.75); border-radius:8px; font-size:1.35em; color:#1e3a5f; text-decoration:none;">javascript <sup style="font-size:0.6em;">3</sup></a>
      <a href="/tags/hacktoberfest/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.75); border-radius:8px; font-size:1.35em; color:#1e3a5f; text-decoration:none;">hacktoberfest <sup style="font-size:0.6em;">3</sup></a>
      <a href="/tags/awesome-list/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.75); border-radius:8px; font-size:1.35em; color:#1e3a5f; text-decoration:none;">awesome-list <sup style="font-size:0.6em;">3</sup></a>
      <a href="/tags/deep-learning/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.75); border-radius:8px; font-size:1.35em; color:#1e3a5f; text-decoration:none;">deep-learning <sup style="font-size:0.6em;">3</sup></a>
      <a href="/tags/python/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.75); border-radius:8px; font-size:1.35em; color:#1e3a5f; text-decoration:none;">python <sup style="font-size:0.6em;">3</sup></a>
      <a href="/tags/chatgpt/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.75); border-radius:8px; font-size:1.35em; color:#1e3a5f; text-decoration:none;">chatgpt <sup style="font-size:0.6em;">3</sup></a>
      <a href="/tags/ai-agents/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.75); border-radius:8px; font-size:1.35em; color:#1e3a5f; text-decoration:none;">ai-agents <sup style="font-size:0.6em;">3</sup></a>
      <a href="/tags/education/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.67); border-radius:8px; font-size:1.13em; color:#1e3a5f; text-decoration:none;">education <sup style="font-size:0.6em;">2</sup></a>
      <a href="/tags/awesome/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.67); border-radius:8px; font-size:1.13em; color:#1e3a5f; text-decoration:none;">awesome <sup style="font-size:0.6em;">2</sup></a>
      <a href="/tags/machine-learning/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.67); border-radius:8px; font-size:1.13em; color:#1e3a5f; text-decoration:none;">machine-learning <sup style="font-size:0.6em;">2</sup></a>
      <a href="/tags/artificial-intelligence/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.67); border-radius:8px; font-size:1.13em; color:#1e3a5f; text-decoration:none;">artificial-intelligence <sup style="font-size:0.6em;">2</sup></a>
      <a href="/tags/automation/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.67); border-radius:8px; font-size:1.13em; color:#1e3a5f; text-decoration:none;">automation <sup style="font-size:0.6em;">2</sup></a>
      <a href="/tags/cli/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.67); border-radius:8px; font-size:1.13em; color:#1e3a5f; text-decoration:none;">cli <sup style="font-size:0.6em;">2</sup></a>
      <a href="/tags/go/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.67); border-radius:8px; font-size:1.13em; color:#1e3a5f; text-decoration:none;">go <sup style="font-size:0.6em;">2</sup></a>
      <a href="/tags/golang/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.67); border-radius:8px; font-size:1.13em; color:#1e3a5f; text-decoration:none;">golang <sup style="font-size:0.6em;">2</sup></a>
      <a href="/tags/deepseek/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.67); border-radius:8px; font-size:1.13em; color:#1e3a5f; text-decoration:none;">deepseek <sup style="font-size:0.6em;">2</sup></a>
      <a href="/tags/gemma/" style="display:inline-block; padding:3px 10px; background:rgba(59,130,246,0.67); border-radius:8px; font-size:1.13em; color:#1e3a5f; text-decoration:none;">gemma <sup style="font-size:0.6em;">2</sup></a>
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
<script>
new Chart(document.getElementById('langChart'), {
  type: 'doughnut',
  data: {
    labels: ["Python", "TypeScript", "JavaScript", "Go", "Shell", "C", "C++", "Dart", "MDX", "HTML"],
    datasets: [{ data: [11, 7, 2, 2, 2, 1, 1, 1, 1, 1], backgroundColor: ["#3572A5", "#3178c6", "#f1e05a", "#00ADD8", "#89e051", "#555555", "#f34b7d", "#00B4AB", "#9ca3af", "#e34c26"] }]
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
    labels: ["freeCodeCamp", "free-programming-boo", "developer-roadmap", "awesome-selfhosted", "react", "openclaw", "linux", "tensorflow", "vscode", "AutoGPT"],
    datasets: [{ label: 'Stars', data: [437589, 383246, 349876, 275759, 243359, 238787, 219766, 193936, 182144, 182098], backgroundColor: '#f59e0b', borderRadius: 4 }]
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
    labels: ["openclaw", "superpowers", "skills", "everything-claude-co", "nanobot", "oh-my-opencode", "ui-ux-pro-max-skill", "awesome-claude-skill", "linux", "n8n"],
    datasets: [{ label: 'Star Change', data: [3753, 1348, 1103, 644, 544, 375, 335, 330, 237, 173], backgroundColor: ["#16a34a", "#16a34a", "#16a34a", "#16a34a", "#16a34a", "#16a34a", "#16a34a", "#16a34a", "#16a34a", "#16a34a"], borderRadius: 4 }]
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
    labels: ["02-25", "02-26", "02-27", "02-28"],
    datasets: [{ label: 'New Repos', data: [0, 2, 4, 4], backgroundColor: '#8b5cf6', borderRadius: 4 }]
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
    labels: ["02-25", "02-26", "02-27", "02-28"],
    datasets: [{"label": "Python", "data": [7, 7, 9, 11], "borderColor": "#3572A5", "backgroundColor": "#3572A533", "fill": true, "tension": 0.3}, {"label": "TypeScript", "data": [7, 7, 7, 7], "borderColor": "#f1e05a", "backgroundColor": "#f1e05a33", "fill": true, "tension": 0.3}, {"label": "JavaScript", "data": [2, 2, 2, 2], "borderColor": "#3178c6", "backgroundColor": "#3178c633", "fill": true, "tension": 0.3}, {"label": "Go", "data": [1, 1, 2, 2], "borderColor": "#dea584", "backgroundColor": "#dea58433", "fill": true, "tension": 0.3}, {"label": "Shell", "data": [2, 2, 2, 2], "borderColor": "#00ADD8", "backgroundColor": "#00ADD833", "fill": true, "tension": 0.3}]
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
    datasets: [{ label: 'Pushes', data: [0, 0, 1, 3, 8, 18, 0], backgroundColor: ["rgba(59, 130, 246, 0.2)", "rgba(59, 130, 246, 0.2)", "rgba(59, 130, 246, 0.2)", "rgba(59, 130, 246, 0.2)", "rgba(59, 130, 246, 0.4444444444444444)", "rgba(59, 130, 246, 1.0)", "rgba(59, 130, 246, 0.2)"], borderRadius: 4 }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
  }
});
</script>

## Trending Repositories {#trending-repositories}

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

<p style="font-size:0.8em; color:#9ca3af;">
Data from <a href="https://github.com">GitHub</a> Search API &middot; Updated: {{ site.data.github.generated_at }}
</p>
